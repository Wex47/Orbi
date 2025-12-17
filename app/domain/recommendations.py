# app/domain/destination_experiences.py

from typing import List, Dict
from app.domain.amadeus_client import AmadeusClient


def get_top_k_destination_experiences(
    client: AmadeusClient,
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
