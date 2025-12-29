from __future__ import annotations
from datetime import date
from typing import List, Dict, Any, Optional
from app.infrastructure.amadeus_client import get_amadeus_client

"""
Domain logic for flight search using Amadeus API.
Fetches flight offers and normalizes the data for consumption."""

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

FLIGHT_OFFERS_PATH = "/v2/shopping/flight-offers"

# ------------------------------------------------------------
# Errors
# ------------------------------------------------------------

class FlightSearchError(RuntimeError):
    pass

# ------------------------------------------------------------
# Internal helpers (private to this domain)
# ------------------------------------------------------------

def _fetch_flight_offers(
    origin: str,
    destination: str,
    departure_date: date,
    *,
    return_date: Optional[date],
    adults: int,
    max_results: int,
) -> List[Dict[str, Any]]:
    try:
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

        return response.get("data", [])

    except Exception as exc:
        raise FlightSearchError(
            "Failed to fetch flight offers from Amadeus"
        ) from exc


def _normalize_offers(
    raw_offers: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    offers: List[Dict[str, Any]] = []

    for item in raw_offers:
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

# ------------------------------------------------------------
# Public domain API
# ------------------------------------------------------------

def search_flights(
    origin: str,
    destination: str,
    departure_date: date,
    *,
    return_date: Optional[date] = None,
    adults: int = 1,
    max_results: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search for flight offers between two locations.

    inputs:
        origin: IATA code of the origin airport
        destination: IATA code of the destination airport
        departure_date: Date of departure
        return_date: Optional date of return
        adults: Number of adult passengers
        max_results: Maximum number of flight offers to return
    
    outputs:
        List of normalized flight offers, each containing:
        - id: Unique identifier for the offer
        - total_price: Total price of the offer
        - currency: Currency of the price
        - duration: Duration of the flight itinerary
        - segments: List of flight segments with departure/arrival details
    """

    raw_offers = _fetch_flight_offers(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        adults=adults,
        max_results=max_results,
    )

    return _normalize_offers(raw_offers)