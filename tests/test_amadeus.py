from dotenv import load_dotenv

from app.domain.amadeus_auth import AmadeusAuth
from app.domain.amadeus_client import AmadeusClient
from app.domain.city_geocoding import get_city_coordinates
from app.domain.recommendations import get_top_k_destination_experiences

load_dotenv()

# Create auth & client ONCE
auth = AmadeusAuth()
client = AmadeusClient(auth)

# 1️⃣ Test city → coordinates
city = get_city_coordinates(
    client=client,
    keyword="PARI",
)

print("City resolved:")
print(city)
print("-" * 50)

if not city:
    raise RuntimeError("City lookup failed")

# 2️⃣ Test coordinates → recommendations
recommendations = get_top_k_destination_experiences(
    client=client,
    latitude=city["latitude"],
    longitude=city["longitude"],
    k=3,
)

print("Top recommendations:")
for idx, r in enumerate(recommendations, start=1):
    print(
        f"{idx}. {r['name']} | "
        f"description: {r["description"]}"
        f"rating={r['rating']} | "
        f"price={r['price']} {r['currency']}"
    )