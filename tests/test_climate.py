from dotenv import load_dotenv

from app.domain.climate import fetch_climate_data

load_dotenv()

result = fetch_climate_data(
    place_name="Paris",
    month="june",
)

print("\nClimate domain result:")
print(result)