
from typing import Optional, Dict, Any
from typing import Optional, Dict, Any
from app.infrastructure.amadeus_client import get_amadeus_client


def get_city_coordinates(
    keyword: str,
    *,
    country_code: Optional[str] = None,
    max_results: int = 1,
) -> Dict[str, Any]:
    """
    Finds a city using Amadeus City Search API and returns its coordinates.

    Returns either:
    - city data dict
    - or {"error": "...", ...}
    """

    client = get_amadeus_client()

    params = {
        "keyword": keyword,
        "max": max_results,
    }

    if country_code:
        params["countryCode"] = country_code

    response = client.get(
        "/v1/reference-data/locations/cities",
        params=params,
    )

    # 🔴 NEW: handle API / network errors
    if "error" in response:
        return {
            "error": "City lookup failed",
            "provider": "amadeus",
            "query": keyword,
            "details": response,
        }

    data = response.get("data", [])

    if not data:
        return {
            "error": "City not found",
            "provider": "amadeus",
            "query": keyword,
        }

    city = data[0]
    geo = city.get("geoCode", {})

    return {
        "name": city.get("name"),
        "iata_code": city.get("iataCode"),
        "country_code": city.get("address", {}).get("countryCode"),
        "latitude": geo.get("latitude"),
        "longitude": geo.get("longitude"),
    }


# app/domain/destination_experiences.py

from typing import List, Dict
from app.infrastructure.amadeus_client import get_amadeus_client


def get_top_k_destination_experiences(
    latitude: float,
    longitude: float,
    radius_km: int = 1,
    k: int = 5,
) -> List[Dict]:
    """
    Returns top-k destination experiences (activities) near a location,
    ranked primarily by rating (descending).

    Args:
        client: AmadeusClient dependency
        latitude: Latitude of the destination
        longitude: Longitude of the destination
        radius_km: Search radius in kilometers
        k: Number of recommendations to return

    Returns:
        List of activity dicts sorted by quality
    """
    
    client = get_amadeus_client()

    response = client.get(
        "/v1/shopping/activities",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius_km,
        },
    )

    activities = []

    for item in response.get("data", []):
        activities.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "description": item.get("shortDescription"),
                "rating": float(item["rating"]) if item.get("rating") else 0.0,
                "price": float(item["price"]["amount"])
                if item.get("price")
                else None,
                "currency": item["price"]["currencyCode"]
                if item.get("price")
                else None,
                "latitude": float(item["geoCode"]["latitude"]),
                "longitude": float(item["geoCode"]["longitude"]),
                "booking_link": item.get("bookingLink")
            }
        )

    # Sort by rating DESC, then by price ASC (optional secondary signal)
    activities.sort(
        key=lambda x: (
            x["rating"],
            -x["price"] if x["price"] is not None else float("-inf"),
        ),
        reverse=True,
    )

    return activities[:k]



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
