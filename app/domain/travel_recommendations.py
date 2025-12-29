from __future__ import annotations
from typing import Optional, Dict, Any, List
from app.infrastructure.amadeus_client import get_amadeus_client

"""
Domain logic for travel recommendations using Amadeus API.
Resolves a city to coordinates and returns nearby destination experiences.
"""

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

CITY_SEARCH_PATH = "/v1/reference-data/locations/cities"
ACTIVITIES_PATH = "/v1/shopping/activities"

# ------------------------------------------------------------
# Errors
# ------------------------------------------------------------

class TravelRecommendationError(RuntimeError):
    pass

# ------------------------------------------------------------
# Fetch & normalize
# ------------------------------------------------------------

def _fetch_city(
    keyword: str,
    *,
    country_code: Optional[str],
    max_results: int,
) -> Dict[str, Any]:
    try:
        client = get_amadeus_client()

        params = {
            "keyword": keyword,
            "max": max_results,
        }
        if country_code:
            params["countryCode"] = country_code

        response = client.get(CITY_SEARCH_PATH, params=params)
        data = response.get("data", [])

        if not data:
            raise TravelRecommendationError(
                f"City not found: '{keyword}'"
            )

        city = data[0]
        geo = city.get("geoCode", {})

        return {
            "name": city.get("name"),
            "iata_code": city.get("iataCode"),
            "country_code": city.get("address", {}).get("countryCode"),
            "latitude": geo.get("latitude"),
            "longitude": geo.get("longitude"),
        }

    except Exception as exc:
        if isinstance(exc, TravelRecommendationError):
            raise
        raise TravelRecommendationError(
            "Failed to resolve city coordinates"
        ) from exc


def _fetch_activities(
    latitude: float,
    longitude: float,
    *,
    radius_km: int,
) -> List[Dict[str, Any]]:
    try:
        client = get_amadeus_client()

        response = client.get(
            ACTIVITIES_PATH,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius_km,
            },
        )

        activities: List[Dict[str, Any]] = []

        for item in response.get("data", []):
            activities.append(
                {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "description": item.get("shortDescription"),
                    "rating": float(item["rating"])
                    if item.get("rating")
                    else 0.0,
                    "price": float(item["price"]["amount"])
                    if item.get("price")
                    else None,
                    "currency": item["price"]["currencyCode"]
                    if item.get("price")
                    else None,
                    "latitude": float(item["geoCode"]["latitude"]),
                    "longitude": float(item["geoCode"]["longitude"]),
                    "booking_link": item.get("bookingLink"),
                }
            )

        # Sort by rating DESC, then price ASC
        activities.sort(
            key=lambda x: (
                x["rating"],
                -x["price"] if x["price"] is not None else float("-inf"),
            ),
            reverse=True,
        )

        return activities

    except Exception as exc:
        raise TravelRecommendationError(
            "Failed to fetch destination activities"
        ) from exc

# ------------------------------------------------------------
# Public domain API
# ------------------------------------------------------------

def get_travel_recommendations(
    city: str,
    *,
    country_code: Optional[str] = None,
    k: int = 5,
    radius_km: int = 10,
) -> Dict[str, Any]:
    """
    Return top-k destination experiences for a given city.
    inputs:
    - city: City name (e.g., "Paris")
    - country_code: Optional ISO country code to disambiguate (e.g., "FR")
    - k: Number of recommendations to return (default: 5)
    - radius_km: Search radius in kilometers (default: 10)
    outputs:
    - dict with city info and list of recommended activities
    """

    city_data = _fetch_city(
        keyword=city,
        country_code=country_code,
        max_results=1,
    )

    activities = _fetch_activities(
        latitude=city_data["latitude"],
        longitude=city_data["longitude"],
        radius_km=radius_km,
    )

    return {
        "city": city_data["name"],
        "country_code": city_data["country_code"],
        "recommendations": activities[:k],
    }