
# from typing import Optional, Dict
# from app.infrastructure.amadeus_client import get_amadeus_client

# def get_city_coordinates(
#     keyword: str,
#     *,
#     country_code: Optional[str] = None,
#     max_results: int = 1,
# ) -> Optional[Dict]:
#     """
#     Finds a city using Amadeus City Search API and returns its coordinates.

#     Args:
#         client: AmadeusAuth dependency
#         keyword: Partial or full city name (3–10 chars)
#         country_code: ISO 3166-1 alpha-2 country code (e.g. "FR")
#         max_results: Max number of search results

#     Returns:
#         {
#             "name": "Paris",
#             "iata_code": "PAR",
#             "country_code": "FR",
#             "latitude": 48.85341,
#             "longitude": 2.3488
#         }
#         or None if no city found
#     """

#     client = get_amadeus_client()

#     params = {
#         "keyword": keyword,
#         "max": max_results,
#     }

#     if country_code:
#         params["countryCode"] = country_code

#     response = client.get(
#         "/v1/reference-data/locations/cities",
#         params=params,
#     )

#     data = response.get("data", [])

#     if not data:
#         return None

#     # Take the top result (Amadeus ranks relevance for us)
#     city = data[0]

#     geo = city.get("geoCode", {})

#     return {
#         "name": city.get("name"),
#         "iata_code": city.get("iataCode"),
#         "country_code": city.get("address", {}).get("countryCode"),
#         "latitude": geo.get("latitude"),
#         "longitude": geo.get("longitude"),
#     }


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
