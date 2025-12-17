from langchain.tools import tool
from app.domain.geo import geocode_place
from app.domain.climate import get_monthly_climate_by_coords
from app.domain.travel_recommendations import (
    create_travel_recommendations_tool
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


#########################

travel_recommendations = create_travel_recommendations_tool()

@tool
def travel_recommendations_tool(
    city: str,
    country_code: str | None = None,
    k: int = 5,
):
    """
    Get top travel experiences for a city.
    """
    return travel_recommendations(
        city=city,
        country_code=country_code,
        k=k,
    )


########################################


from langchain.tools import tool
from app.domain.flight_search_tool import create_flight_search_tool

flight_search = create_flight_search_tool()

@tool
def search_flights_tool(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str | None = None,
    adults: int = 1,
    max_results: int = 5,
):
    """
    Search for flight offers between two cities.
    Dates must be in YYYY-MM-DD format.
    """
    return flight_search(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        adults=adults,
        max_results=max_results,
    )



# app/tools.py

TRAVEL_TOOLS = [
    get_place_climate,
    travel_recommendations_tool,
    search_flights_tool
]