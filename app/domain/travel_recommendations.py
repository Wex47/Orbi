# app/domain/travel_recommendations.py

from typing import Optional, Dict, Any

from app.domain.city_geocoding import get_city_coordinates
from app.domain.recommendations import get_top_k_destination_experiences
from app.domain.amadeus_auth import AmadeusAuth
from app.domain.amadeus_client import AmadeusClient


def create_travel_recommendations_tool() -> callable:
    """
    Factory that creates a travel recommendations tool
    with a shared Amadeus client and cached OAuth token.
    """

    # Created ONCE per process
    auth = AmadeusAuth()
    client = AmadeusClient(auth)

    def travel_recommendations_tool(
        city: str,
        *,
        country_code: Optional[str] = None,
        k: int = 5,
        radius_km: int = 2,
    ) -> Dict[str, Any]:
        """
        Returns top-k destination experiences for a given city.
        """

        city_data = get_city_coordinates(
            client=client,
            keyword=city,
            country_code=country_code,
        )

        if not city_data:
            return {
                "error": f"Could not find city '{city}'"
            }

        experiences = get_top_k_destination_experiences(
            client=client,
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

    return travel_recommendations_tool
