from __future__ import annotations
import logging
from langchain.agents import create_agent
from langchain_core.messages import ToolMessage
from app.infrastructure.llm import get_lightweight_chat_model
from app.tools.tools import TRAVEL_TOOLS
from app.config.settings import settings

logger = logging.getLogger(__name__)

EXECUTOR_SYSTEM = """
You are a travel assistant that plans and executes tasks as needed.

Instructions:
- Reason internally step by step.
- Decide which actions to take without exposing your internal reasoning.
- Use tools when factual or real-world data is required.
- Be explicit in the final answer about what came from tools vs what was inferred.
- Produce a complete, clear, user-facing response.

Do not expose your internal chain-of-thought.
""".strip()

# ------------------------------------------------------------------
# ReAct-style unified executor
# ------------------------------------------------------------------

_AGENT = create_agent(
    model=get_lightweight_chat_model(),
    tools=TRAVEL_TOOLS,
    system_prompt=EXECUTOR_SYSTEM,
)


def executor_node(state: dict) -> dict:
    """
    ReAct-style unified executor, that plans, reasons,
    uses tools and generates final answers.
    """

    try:
        result = _AGENT.invoke(
        {
            "messages": state["messages"]
        }
        )
        logger.debug(settings.SUCCESS_GENERIC)

    except Exception as exc:
        logger.exception(settings.FAILED_GENERIC)
        raise exc
    

    messages = result.get("messages", [])

    # Detect whether tools were used in during this invocation
    tools_used = any(
        (
            (isinstance(m, dict) and m.get("role") == "tool")
            or isinstance(m, ToolMessage)
        )
        for m in messages
    )

    # Extract final assistant message
    final_text = ""
    if messages:
        last = messages[-1]
        if isinstance(last, dict):
            final_text = last.get("content", "")
        else:
            final_text = getattr(last, "content", "")

    return {
        "execution": final_text,
        "tools_used": tools_used,
    }