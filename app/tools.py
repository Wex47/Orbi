
from langchain.tools import tool

# app/tools.py

import requests
from langchain.tools import tool
from datetime import datetime


# Future enhancement for the weather tools: if the date is close by, check the forecast API:

@tool
def get_monthly_climate(
    latitude: float,
    longitude: float,
    month: int
) -> str:
    """
    Get historical average temperature and precipitation for a given location and month
    using daily ERA5 data (2010–2020).
    """

    if not 1 <= month <= 12:
        return "Month must be between 1 and 12."

    url = "https://archive-api.open-meteo.com/v1/era5"

    #TODO: configure the dates?
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": "2010-01-01",
        "end_date": "2020-12-31",
        "daily": [
            "temperature_2m_mean",
            "precipitation_sum"
        ],
        "timezone": "UTC"
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        dates = data["daily"]["time"]
        temps = data["daily"]["temperature_2m_mean"]
        rain = data["daily"]["precipitation_sum"]

        month_temps = []
        month_rain = []

        for d, t, r in zip(dates, temps, rain):
            if datetime.fromisoformat(d).month == month:
                month_temps.append(t)
                month_rain.append(r)

        avg_temp = round(sum(month_temps) / len(month_temps), 1)
        avg_rain = round(sum(month_rain) / len(set(
            datetime.fromisoformat(d).year for d in dates
            if datetime.fromisoformat(d).month == month
        )), 1)

        return (
            f"For month {month}, the historical average temperature is "
            f"{avg_temp}°C with {avg_rain} mm of precipitation."
        )

    except Exception as e:
        return f"Failed to fetch climate data: {str(e)}"



@tool
def geocode_place(place_name: str) -> str:
    """
    Convert a place name (city, region, or country) into latitude and longitude.
    Useful as a first step before fetching climate data.
    """

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": place_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return f"No coordinates found for '{place_name}'."

        result = data["results"][0]

        lat = result["latitude"]
        lon = result["longitude"]
        name = result["name"]
        country = result.get("country", "Unknown")

        return (
            f"Coordinates for {name}, {country}: "
            f"latitude {lat}, longitude {lon}."
        )

    except Exception as e:
        return f"Failed to geocode place: {str(e)}"

