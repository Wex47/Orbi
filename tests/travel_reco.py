# scripts/test_travel_recommendations_manual.py

from app.domain import travel_recommendations as tr


# --- override dependencies ---

def fake_get_city_coordinates(keyword, country_code=None):
    return {
        "name": "Paris",
        "country_code": "FR",
        "latitude": 48.8566,
        "longitude": 2.3522,
    }


def fake_get_top_k_destination_experiences(latitude, longitude, k, radius_km):
    return [
        {"name": "Eiffel Tower", "type": "landmark"},
        {"name": "Louvre Museum", "type": "museum"},
    ]


tr.get_city_coordinates = fake_get_city_coordinates
tr.get_top_k_destination_experiences = fake_get_top_k_destination_experiences


# --- run ---

result = tr.get_travel_recommendations(
    city="Paris",
    k=2,
)

print("\nTravel recommendations result:")
print(result)
