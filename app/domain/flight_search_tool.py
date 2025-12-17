# app/tools/flight_search_tool.py

from datetime import date
from typing import Optional, Dict, Any

from app.domain.amadeus_auth import AmadeusAuth
from app.domain.amadeus_client import AmadeusClient
from app.domain.flight_search import search_flights


def create_flight_search_tool():
    """
    Creates a flight search tool with a shared Amadeus client.
    """

    # 🔒 Created ONCE
    auth = AmadeusAuth()
    client = AmadeusClient(auth)

    def flight_search_tool(
        origin: str,
        destination: str,
        departure_date: str,
        *,
        return_date: Optional[str] = None,
        adults: int = 1,
        max_results: int = 5,
    ) -> Dict[str, Any]:
        flights = search_flights(
            client=client,
            origin=origin,
            destination=destination,
            departure_date=date.fromisoformat(departure_date),
            return_date=date.fromisoformat(return_date) if return_date else None,
            adults=adults,
            max_results=max_results,
        )

        return {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "flights": flights,
        }

    return flight_search_tool
