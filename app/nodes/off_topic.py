
from __future__ import annotations

def off_topic_node(state: dict) -> dict:

    OFF_TOPIC_RESPONSE = (
        "That’s outside my scope, but I’d love to help with travel! "
        "Ask me about flights, destinations, weather, or trip planning, "
        "and we can get started."
    )

    return {
        "execution": OFF_TOPIC_RESPONSE,
        "verified": True,
        "tools_used": False,
    }
