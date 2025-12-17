# app/domain/flight_search.py

from typing import List, Dict, Any
from datetime import date

def search_flights(
    client,
    origin: str,
    destination: str,
    departure_date: date,
    *,
    return_date: date | None = None,
    adults: int = 1,
    max_results: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search flight offers between two cities.
    """

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date.isoformat(),
        "adults": adults,
        "max": max_results,
    }

    if return_date:
        params["returnDate"] = return_date.isoformat()

    print(params)
    response = client.get(
        "/v2/shopping/flight-offers",
        params=params,
    )

    offers = []

    for item in response.get("data", []):
        price = item.get("price", {})
        itinerary = item["itineraries"][0]
        segments = itinerary["segments"]

        offers.append({
            "id": item.get("id"),
            "total_price": price.get("total"),
            "currency": price.get("currency"),
            "duration": itinerary.get("duration"),
            "segments": [
                {
                    "from": s["departure"]["iataCode"],
                    "to": s["arrival"]["iataCode"],
                    "departure": s["departure"]["at"],
                    "arrival": s["arrival"]["at"],
                    "carrier": s.get("carrierCode"),
                    "flight_number": s.get("number"),
                }
                for s in segments
            ],
        })

    return offers