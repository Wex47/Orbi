from __future__ import annotations
from app.infrastructure.llm import get_lightweight_chat_model
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)


DIRECT_SYSTEM = """
You are a professional travel assistant.
Answer conversationally and helpfully.

Special rule:
- If the query is not related to travel, let them know you cannot provide off-topic responses.

""".strip()


def direct_node(state: dict) -> dict:
    """
    Direct answer node for simple travel-related queries,
    such as general travel advice, information that doesn't require tool usage,
    or questions that can be answered from conversation context alone.
    """

    model = get_lightweight_chat_model()
    messages = [{"role": "system", "content": DIRECT_SYSTEM}] + state["messages"]
    
    try:
        response = model.invoke(messages).content
        logger.debug(settings.SUCCESS_GENERIC)

    except Exception as exc:
        logger.exception(settings.FAILED_GENERIC)
        raise exc

    return {
        "execution": response,
        "verified": False,
    }