from dotenv import load_dotenv

from app.domain.recommendations.travel_recommendations import (
    create_travel_recommendations_tool,
)

load_dotenv()

travel_recommendations = create_travel_recommendations_tool()

result = travel_recommendations(
    city="Toky",
    k=3,
)

import pprint
pprint.pprint(result)

