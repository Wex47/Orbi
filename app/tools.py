from langchain.tools import tool
from app.domain.geo import geocode_place
from app.domain.climate import get_monthly_climate_by_coords

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
