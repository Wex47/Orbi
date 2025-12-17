from typing import Optional, Dict, Any
from app.domain.recommendations.city_geocoding import get_city_coordinates
from app.domain.recommendations.recommendations import get_top_k_destination_experiences


def get_travel_recommendations(
    city: str,
    *,
    country_code: Optional[str] = None,
    k: int = 5,
    radius_km: int = 2,
) -> Dict[str, Any]:
    """
    Return top-k recommended destination experiences for a given city.

    The function resolves the city name to geographic coordinates
    and then retrieves nearby destination experiences.
    """

    city_data = get_city_coordinates(
        keyword=city,
        country_code=country_code,
    )

    if not city_data or "error" in city_data:
        return {"error": f"Could not find city '{city}'"}

    experiences = get_top_k_destination_experiences(
        latitude=city_data["latitude"],
        longitude=city_data["longitude"],
        k=k,
        radius_km=radius_km,
    )

    return {
        "city": city_data["name"],
        "country_code": city_data["country_code"],
        "recommendations": experiences,
    }
