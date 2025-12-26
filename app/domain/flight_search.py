# flight_search.py

from datetime import date
from typing import List, Dict, Any
from app.infrastructure.amadeus_client import get_amadeus_client

FLIGHT_OFFERS_PATH = "/v2/shopping/flight-offers"

def search_flights(
    origin: str,
    destination: str,
    departure_date: date,
    *,
    return_date: date | None = None,
    adults: int = 1,
    max_results: int = 5,
) -> List[Dict[str, Any]]:
    client = get_amadeus_client()

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date.isoformat(),
        "adults": adults,
        "max": max_results,
    }

    if return_date:
        params["returnDate"] = return_date.isoformat()

    response = client.get(FLIGHT_OFFERS_PATH, params=params)

    offers = []
    for item in response.get("data", []):
        itinerary = item["itineraries"][0]
        segments = itinerary["segments"]

        offers.append({
            "id": item.get("id"),
            "total_price": item["price"]["total"],
            "currency": item["price"]["currency"],
            "duration": itinerary["duration"],
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
