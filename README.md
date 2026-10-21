# Python Weather App

## Description
A command-line weather application that retrieves live weather information using the OpenWeather API.

## Features
- Current temperature in Celsius
- Humidity and feels-like temperature
- Current weather conditions
- Short weather forecast
- Error handling for unknown cities and API failures
- Ten-minute in-memory cache to reduce repeated requests
- API key loaded securely from an environment file

## Technologies
- Python 3.10+
- Requests
- python-dotenv
- OpenWeather API

## Installation
Install dependencies:

`pip install requests python-dotenv`

Create a `.env` file containing:

`OPENWEATHER_KEY=your_api_key_here`

Replace the placeholder with your own API key.

## Run
`python weather_app.py`

## API Key Security
The API key is stored in `.env`, loaded through python-dotenv, and excluded from Git using `.gitignore`. The key is not included in the source code or README.

## Data Source
OpenWeather: https://openweathermap.org/

## Testing
Test a valid city, an unknown city, an empty input, an unavailable API key, and a network connection failure.
