from dotenv import load_dotenv
from datetime import date, timedelta
from pprint import pprint

from app.infrastructure.amadeus_auth import AmadeusAuth
from app.infrastructure.amadeus_client_impl import AmadeusClient
from app.domain.flights.flight_search import search_flights

load_dotenv()

# auth = AmadeusAuth()
# client = AmadeusClient(auth)

# flights = search_flights(
#     client=client,
#     origin="BOS",
#     destination="CHI",
#     departure_date=date.today() + timedelta(days=14),
#     adults=1,
#     max_results=10,
# )

# print("Flight search domain result:")
# for f in flights:
#     pprint(f)


from app.domain.flights.flight_search_tool import create_flight_search_tool

flight_search = create_flight_search_tool()

tool_result = flight_search(
    origin="TLV",
    destination="DXB",
    departure_date="2026-01-01",
    adults=1,
    max_results=3,
)

print("\nUnified flight search tool result:")
print(tool_result)
