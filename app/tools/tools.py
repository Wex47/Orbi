from langchain.tools import tool
from app.domain.climate.geo import geocode_place
from app.domain.climate.climate import get_monthly_climate_by_coords
from datetime import date
from typing import Optional
from app.domain.recommendations.travel_recommendations import (
    get_travel_recommendations,
)

@tool
def get_place_climate(place_name: str, month: str) -> str:
    """
    Get historical climate details for a place and month.
    """

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


########################################

from app.domain.flights.flight_search import search_flights

@tool
def search_flights_tool(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    adults: int = 1,
    max_results: int = 5,
):
    """
    Search for available commercial flight offers between two cities.

    Inputs use IATA airport or city codes (e.g., "TLV", "JFK").
    Dates must be in YYYY-MM-DD format.
    Returns flight options with price, duration, and segment details.
    Use when the user asks about flight availability, prices, or routes.
    """
    return search_flights(
        origin=origin,
        destination=destination,
        departure_date=date.fromisoformat(departure_date),
        return_date=date.fromisoformat(return_date) if return_date else None,
        adults=adults,
        max_results=max_results,
    )


#########################


@tool
def travel_recommendations_tool(
    city: str,
    country_code: Optional[str] = None,
    k: int = 5,
):
    """
    Get top recommended travel experiences for a given city.

    Resolves the city name to geographic coordinates and returns nearby
    attractions and points of interest.
    Use when the user asks what to see or do in a destination.
    """
    return get_travel_recommendations(
        city=city,
        country_code=country_code,
        k=k,
    )


########################################


from app.domain.time.timezone_service import get_current_time_by_timezone

@tool
def get_current_time(timezone: str) -> dict:
    """
    Retrieve the current local time and timezone metadata using a real-time API.

    IMPORTANT:
    - This tool PROVIDES real-time information.
    - Use this tool whenever the user asks for the current time, date,
      or timezone information for any location.
    - Do NOT answer such questions without calling this tool.
    - Do NOT state that you lack real-time access if this tool is available.

    Input:
        timezone (str): Timezone in Area/Location or Area/Location/Region format.
                        Examples:
                        - "Europe/London"
                        - "Asia/Tokyo"
                        - "America/Argentina/Salta"

    Output:
        {
            "abbreviation": str,
            "datetime": str,
            "day_of_week": int,
            "day_of_year": int,
            "dst": bool,
            "dst_from": str | null,
            "dst_offset": int,
            "dst_until": str | null,
            "raw_offset": int,
            "timezone": str,
            "unixtime": int,
            "utc_datetime": str,
            "utc_offset": str,
            "week_number": int
        }
    """
    return get_current_time_by_timezone(timezone)




#########################################

TRAVEL_TOOLS = [
    get_place_climate,
    travel_recommendations_tool,
    search_flights_tool,
    get_current_time
]