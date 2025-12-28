from __future__ import annotations
from typing import Dict, Any
from app.infrastructure.llm import get_lightweight_chat_model
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

ROUTER_SYSTEM = """
You are a routing component for a travel assistant.

Your task is to classify the user's request into exactly ONE of the following routes:

OFF_TOPIC:
- The request is not related to travel at all.
- Examples: programming questions, math problems, personal advice, meta questions.

DIRECT:
- The request is travel-related.
- It can be answered directly in a single step.
- No external tools or multi-step reasoning are required.

PLAN:
- The request is travel-related.
- It requires multiple steps, planning, comparisons, or external factual data
  (e.g., flights, weather, costs, itineraries).

Rules:
- If the request is NOT travel-related, choose OFF_TOPIC.
- If the request is travel-related and simple, choose DIRECT.
- If the request is travel-related and complex, choose PLAN.
- If you are unsure, choose PLAN.

Return ONLY one word: OFF_TOPIC, DIRECT, or PLAN.
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