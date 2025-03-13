"""This module defines the main entry point for the Apify Actor.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from __future__ import annotations

from dotenv import load_dotenv
from apify import Actor
from crewai import Agent, Crew, Task, LLM
import datetime
from src.kayak import kayak
from src.browserbase import browserbase
import os

load_dotenv()


async def main() -> None:
    """Main entry point for the Apify Actor.

    This coroutine is executed using `asyncio.run()`, so it must remain an asynchronous function for proper execution.
    Asynchronous execution is required for communication with the Apify platform, and it also enhances performance in
    the field of web scraping significantly.

    Raises:
        ValueError: If the input is missing required attributes.
    """
    async with Actor:
        # Charge for Actor start
        await Actor.charge('actor-start')

        # Handle input
        actor_input = await Actor.get_input()

        # Provide default values if not present
        origin = actor_input.get('origin', 'JFK')
        destination = actor_input.get('destination', 'LAX')
        date = actor_input.get('date', '2025-03-10')
        model_name = actor_input.get('modelName', 'gpt-4o-mini')

        if not all([origin, destination, date]):
            msg = 'Missing required input parameters (origin, destination, date)!'
            raise ValueError(msg)
        
        # Load Browserbase API key and project ID from input or fallback to .env
        browserbase_api_key = actor_input.get('BROWSERBASE_API_KEY', os.environ['BROWSERBASE_API_KEY'])
        browserbase_project_id = actor_input.get('BROWSERBASE_PROJECT_ID', os.environ['BROWSERBASE_PROJECT_ID'])

        # Check if both API key and project ID are provided
        if browserbase_api_key and browserbase_project_id:
            os.environ['BROWSERBASE_API_KEY'] = browserbase_api_key
            os.environ['BROWSERBASE_PROJECT_ID'] = browserbase_project_id


        request = f"flights from {origin} to {destination} on {date}"

        flight_agent = Agent(
            role='Flight Search Expert',
            goal='Find the best flight options for travelers',
            backstory=(
                'I am an expert in finding and analyzing flight options. '
                'I help users find the most suitable flights based on their preferences.'
            ),
            # tools=tools,  # Ensure this is a list of valid tool instances
            tools = [kayak, browserbase],
            verbose=True,
            llm=model_name
        )

        summarize_agent = Agent(
            role='Flight Summary Expert',
            goal='Summarize flight options and provide recommendations',
            backstory=(
                'I analyze flight options and provide clear summaries and recommendations '
                'to help users make the best choice.'
            ),
            verbose=True,
            llm=model_name
        )

        # Create tasks
        output_search_example = """
            Here are our top 5 flights from San Francisco to New York on 21st September 2025:
            1. Delta Airlines: Departure: 21:35, Arrival: 03:50, Duration: 6 hours 15 minutes, Price: $125, Details: https://www.kayak.com/flights/sfo/jfk/2025-09-21/12:45/13:55/2:10/delta/airlines/economy/1
            """

        search_task = Task(
            description=f"Search flights from {origin} to {destination} on {date}",
            expected_output=output_search_example,
            agent=flight_agent,
        )
        await Actor.charge(event_name='task-completed')
        output_providers_example = """
            Here are our top 5 picks from San Francisco to New York on 21st September 2025:
            1. Delta Airlines:
                - Departure: 21:35
                - Arrival: 03:50
                - Duration: 6 hours 15 minutes
                - Price: $125
                - Booking: [Delta Airlines](https://www.kayak.com/flights/sfo/jfk/2025-09-21/12:45/13:55/2:10/delta/airlines/economy/1)
                ...
        """

        summary_task = Task(
            description='Analyze the flight options and provide recommendations',
            expected_output=output_providers_example,
            agent=summarize_agent,
        )

        # Create and execute crew
        crew = Crew(
            agents=[flight_agent, summarize_agent],
            tasks=[search_task, summary_task],
            max_rpm=100,
            verbose=True,
            planning=True,
        )

        crew_output = crew.kickoff(inputs={
                        "request": request,
                        "current_year": datetime.date.today().year,
        })

        raw_response = crew_output.raw

        # Log total token usage
        Actor.log.info('Total tokens used: %s', crew_output.token_usage.total_tokens)

        await Actor.charge('task-completed')

        # Push results to the dataset
        await Actor.push_data({
            'origin': origin,
            'destination': destination,
            'date': date,
            'results': raw_response,
        })
        Actor.log.info('Pushed the data into the dataset!')