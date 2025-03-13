# Flight Search Agent

This project implements a flight search agent using the CrewAI framework and Apify Actors. The agent is designed to search for flights, summarize options, and provide recommendations based on user input.

## Overview

The Flight Search Agent utilizes the Apify SDK to interact with web services and gather flight data. It leverages the CrewAI framework to manage agents and tasks, allowing for efficient processing and summarization of flight options.

## Features

- **Flight Search**: The agent can search for flights between specified origins and destinations on given dates using the Kayak tool.
- **Flight Summarization**: It summarizes the search results and provides recommendations to users.
- **Environment Configuration**: The agent uses environment variables for sensitive information like API keys.
- **Asynchronous Execution**: The main function is asynchronous, allowing for efficient web scraping and data processing.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Required packages listed in `requirements.txt`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Arindam200/flight-finder
   cd flight-finder
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables. Create a `.env` file based on the `.env.example` template:
   ```bash
   cp .env.example .env
   ```

4. Fill in your API keys in the `.env` file.

### Running the Agent

To run the agent, use the following command:
```bash
apify run
```

### Input Schema

The agent expects input in the following JSON format:
```json
{
    "query": "Analyze the posts of the @openai and @googledeepmind and summarize me current trends in the AI.",
    "modelName": "gpt-4o-mini",
    "debug": true,
    "BROWSERBASE_API_KEY": "your browserbase api kei",
    "BROWSERBASE_PROJECT_ID": "your browserbase project id"
}
```

### Output

The agent outputs the flight search results in a structured format, which includes:
- Origin
- Destination
- Date
- Results (detailed flight options)

## Tools Used

- **CrewAI**: A framework for building AI agents.
- **Apify SDK**: A toolkit for web scraping and automation.
- **Kayak API**: For searching flight options.
- **Browserbase**: For loading web pages and extracting content.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Apify](https://apify.com) for providing the SDK and platform for building web scrapers.
- [CrewAI](https://www.crewai.com) for the agent framework.