from __future__ import annotations
from datetime import datetime
from collections import defaultdict
from typing import Dict, Any, Union
import requests
from app.config.settings import settings

"""
Domain logic for climate data using Open-Meteo API.
Fetches historical climate data for a given place and month.
Returns average temperature and precipitation.
"""

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
CLIMATE_URL = "https://archive-api.open-meteo.com/v1/era5"

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}

MONTHS_NUM_TO_NAME = {v: k for k, v in MONTHS.items()}

# ------------------------------------------------------------
# Errors
# ------------------------------------------------------------

class ClimateServiceError(RuntimeError):
    pass


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def _normalize_month(month: Union[str, int]) -> tuple[int, str]:
    if isinstance(month, str):
        month_num = MONTHS.get(month.lower())
        if not month_num:
            raise ValueError("Invalid month name.")
        return month_num, month.lower()

    if isinstance(month, int):
        if not 1 <= month <= 12:
            raise ValueError("Month number must be between 1 and 12.")
        return month, MONTHS_NUM_TO_NAME[month]

    raise ValueError("Month must be a string or integer.")


# ------------------------------------------------------------
# Fetch & normalize
# ------------------------------------------------------------

def _geocode(place_name: str) -> Dict[str, Any]:
    try:
        response = requests.get(
            GEOCODE_URL,
            params={
                "name": place_name,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=settings.HTTP_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            raise ClimateServiceError(
                f"No coordinates found for '{place_name}'."
            )

        r = data["results"][0]
        return {
            "name": r["name"],
            "country": r.get("country", "Unknown"),
            "latitude": r["latitude"],
            "longitude": r["longitude"],
        }

    except Exception as exc:
        raise ClimateServiceError("Failed to geocode place") from exc


def _fetch_monthly_climate(
    latitude: float,
    longitude: float,
    month_num: int,
) -> Dict[str, float]:
    try:
        response = requests.get(
            CLIMATE_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "start_date": "2010-01-01",
                "end_date": "2020-12-31",
                "daily": [
                    "temperature_2m_mean",
                    "precipitation_sum",
                ],
                "timezone": "UTC",
            },
            timeout=settings.HTTP_TIMEOUT,
        )
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

        if not month_temps:
            raise ClimateServiceError("No climate data for given month.")

        return {
            "average_temperature_c": round(
                sum(month_temps) / len(month_temps), 1
            ),
            "average_precipitation_mm": round(
                sum(rain_by_year.values()) / len(rain_by_year), 1
            ),
        }

    except Exception as exc:
        raise ClimateServiceError(
            "Failed to fetch climate data"
        ) from exc


# ------------------------------------------------------------
# Public domain API
# ------------------------------------------------------------

def fetch_climate_data(
    place_name: str,
    month: Union[str, int],
) -> Dict[str, Any]:
    """
    Return average historical climate for a place and month.
    inputs:
        place_name: Name of the place (city, town, etc.)
        month: Month name (e.g. "may") or month number (e.g. 5)
    outputs:
        A dictionary with:
        {
            "place": str,          # Normalized place name
            "country": str,        # Country name
            "month": str,          # Month name capitalized
            "average_temperature_c": float,
            "average_precipitation_mm": float,
        }
    """

    month_num, month_name = _normalize_month(month)
    location = _geocode(place_name)
    climate = _fetch_monthly_climate(
        location["latitude"],
        location["longitude"],
        month_num,
    )

    return {
        "place": location["name"],
        "country": location["country"],
        "month": month_name.capitalize(),
        **climate,
    }