import requests

def geocode_place(place_name: str) -> dict:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": place_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        raise ValueError(f"No coordinates found for '{place_name}'.")

    r = data["results"][0]

    return {
        "name": r["name"],
        "country": r.get("country", "Unknown"),
        "latitude": r["latitude"],
        "longitude": r["longitude"],
    }
