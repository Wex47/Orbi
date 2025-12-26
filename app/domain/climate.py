import requests
from datetime import datetime
from collections import defaultdict
from typing import Union

# first function
def geocode_place(place_name: str) -> dict:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": place_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        raise ValueError(f"No coordinates found for '{place_name}'.")

    r = data["results"][0]

    return {
        "name": r["name"],
        "country": r.get("country", "Unknown"),
        "latitude": r["latitude"],
        "longitude": r["longitude"],
    }

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}

MONTHS_NUM_TO_NAME = {v: k for k, v in MONTHS.items()}

# second function
def get_monthly_climate_by_coords(
    latitude: float,
    longitude: float,
    month: Union[str, int],
) -> dict:
    """
    month can be either:
    - month name (e.g. "may")
    - month number (e.g. 5)
    """

    # Normalize month
    if isinstance(month, str):
        month_num = MONTHS.get(month.lower())
        if not month_num:
            raise ValueError("Invalid month name.")
        month_name = month.lower()

    elif isinstance(month, int):
        if not 1 <= month <= 12:
            raise ValueError("Month number must be between 1 and 12.")
        month_num = month
        month_name = MONTHS_NUM_TO_NAME[month]

    else:
        raise ValueError("Month must be a string or integer.")

    url = "https://archive-api.open-meteo.com/v1/era5"

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

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    dates = data["daily"]["time"]
    temps = data["daily"]["temperature_2m_mean"]
    rain = data["daily"]["precipitation_sum"]

    month_temps = []
    rain_by_year = defaultdict(float)

    for d, t, r in zip(dates, temps, rain):
        dt = datetime.fromisoformat(d)
        if dt.month == month_num:
            month_temps.append(t)
            rain_by_year[dt.year] += r

    avg_temp = round(sum(month_temps) / len(month_temps), 1)
    avg_rain = round(
        sum(rain_by_year.values()) / len(rain_by_year),
        1
    )

    return {
        "month": month_name.capitalize(),
        "average_temperature_c": avg_temp,
        "average_precipitation_mm": avg_rain,
    }


def fetch_climate_data(place_name: str, month: str):
    try:
        coords = geocode_place(place_name)
        climate = get_monthly_climate_by_coords(
            coords["latitude"],
            coords["longitude"],
            month
        )

        return (
            f"{coords['name']}, {coords['country']} in {month.capitalize()}:\n"
            f"- Avg temperature: {climate['average_temperature_c']}°C\n"
            f"- Precipitation: {climate['average_precipitation_mm']} mm"
        )

    except Exception as e:
        return str(e)