
from __future__ import annotations
from typing import Dict, Any

def off_topic_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Guardrail - Handles off-topic queries by providing a polite refusal deterministically.
    inputs: 'messages'
    outputs: 'execution', 'verified' (always True), 'tools_used' (always False)
    """

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
