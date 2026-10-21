
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Store successful results temporarily to reduce API requests.
cache = {}
CACHE_SECONDS = 600


def get_weather(city):
    """Fetch current weather and forecast for a city."""
    if not API_KEY:
        print("Error: OPENWEATHER_KEY is missing from .env.")
        return

    city_key = city.strip().casefold()

    if city_key in cache:
        saved_time, saved_data = cache[city_key]
        if time.time() - saved_time < CACHE_SECONDS:
            print("\nShowing cached weather data.")
            display_weather(saved_data)
            return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        # Get current weather.
        response = requests.get(
            f"{BASE_URL}/weather",
            params=params,
            timeout=10
        )

        if response.status_code == 401:
            print("Invalid or inactive API key. Check your key.")
            return

        if response.status_code == 404:
            print("City not found. Check the spelling.")
            return

        response.raise_for_status()
        current = response.json()

        # Get the five-day forecast.
        forecast_response = requests.get(
            f"{BASE_URL}/forecast",
            params=params,
            timeout=10
        )
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        data = {
            "city": current["name"],
            "country": current["sys"]["country"],
            "temperature": current["main"]["temp"],
            "feels_like": current["main"]["feels_like"],
            "humidity": current["main"]["humidity"],
            "description": current["weather"][0]["description"],
            "forecast": forecast_data["list"][:3]
        }

        cache[city_key] = (time.time(), data)
        display_weather(data)

    except requests.exceptions.Timeout:
        print("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        print("Connection error. Check your internet connection.")
    except requests.exceptions.HTTPError as error:
        print("Weather API error:", error)
    except (KeyError, IndexError, TypeError, ValueError):
        print("Could not read the weather data correctly.")


def display_weather(data):
    """Display weather information clearly."""
    print("\n========== WEATHER REPORT ==========")
    print(f"City: {data['city']}, {data['country']}")
    print(f"Temperature: {data['temperature']:.1f} °C")
    print(f"Feels like: {data['feels_like']:.1f} °C")
    print(f"Humidity: {data['humidity']}%")
    print(f"Conditions: {data['description'].title()}")

    print("\n--- SHORT FORECAST ---")

    for item in data["forecast"]:
        date_time = item["dt_txt"]
        temp = item["main"]["temp"]
        description = item["weather"][0]["description"].title()

        print(f"{date_time} | {temp:.1f} °C | {description}")

    print("====================================")


def main():
    print("===== PYTHON WEATHER APP =====")

    while True:
        city = input(
            "\nEnter city name (or type 'quit' to exit): "
        ).strip()

        if city.casefold() == "quit":
            print("Thanks for using the Weather App!")
            break

        if not city:
            print("Please enter a city name.")
            continue

        get_weather(city)


if __name__ == "__main__":
    main()
