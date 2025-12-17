# FACTUAL_KEYWORDS = {
#     "weather", "temperature", "climate", "rain", "snow",
#     "cost", "price", "budget",
#     "distance", "far", "flight time", "duration",
#     "best time", "season",
# }

# def requires_facts(user_input: str) -> bool:
#     text = user_input.lower()
#     return any(k in text for k in FACTUAL_KEYWORDS)


def tools_were_used(result: dict) -> bool:
    return bool(result.get("intermediate_steps"))
