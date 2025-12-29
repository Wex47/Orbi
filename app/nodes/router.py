from __future__ import annotations
from typing import Dict, Any
from app.infrastructure.llm import get_lightweight_chat_model
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

ROUTER_SYSTEM = """
You are a routing classifier for a travel assistant.

Classify the user’s latest message into EXACTLY ONE route:

OFF_TOPIC  
Not primarily about travel.
Examples: coding help, cooking, math, relationships, general trivia, etc.

DIRECT  
Travel-related and can be answered ONLY using:
- Information already present in the conversation, OR
- Stable, non-time-sensitive life knowledge (conceptual or evergreen)

PLAN  
Travel-related and requires ANY of the following:
- Fresh, verified, location-specific, or time-sensitive info
- Multiple steps or structured planning (itineraries, comparisons, options)
- Checking rules, requirements, or advisories

Special rules:
- Not travel related -> OFF_TOPIC
- When unsure, choose PLAN

reason internally. Return EXACTLY ONE word:
OFF_TOPIC | DIRECT | PLAN
""".strip()


def router_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Routes the conversation based on the latest user message.
    Analyzes whether the request is OFF_TOPIC, DIRECT, or PLAN.
    
    inputs: 'messages'
    outputs: 'route', 'query'
    """
    model = get_lightweight_chat_model()

    last_message = state["messages"][-1]
    if isinstance(last_message, dict):
        query = last_message.get("content", "")
    else:
        query = getattr(last_message, "content", "")

    logger.debug(f"Router model will be invoked with the query: {query}")
    messages = [{"role": "system", "content": ROUTER_SYSTEM}] + state["messages"]

    try:
        response = model.invoke(messages, timeout=30)
        out = response.content.strip().upper()
        logger.debug(settings.SUCCESS_GENERIC)

    except Exception as exc:
        logger.exception(settings.FAILED_GENERIC)
        raise exc

    if out.startswith("OFF_TOPIC"):
        route = "OFF_TOPIC"
    elif out.startswith("PLAN"):
        route = "PLAN"
    elif out.startswith("DIRECT"):
        route = "DIRECT"
    else:
        route = "PLAN"

    return {
        "route": route,
        "query": query,
    }