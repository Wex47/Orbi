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


TRAVEL_TOOLS = [
    get_place_climate,
    travel_recommendations_tool,
    search_flights_tool
]