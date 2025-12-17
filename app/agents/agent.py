from __future__ import annotations

from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from app.tools.tools import TRAVEL_TOOLS
from app.config.settings import settings


# -------------------------------------------------------------------
# System Prompt
# -------------------------------------------------------------------

SYSTEM_PROMPT = """
You are a professional travel planning assistant.

Rules:
- Use tools whenever factual data is required.
- Be explicit about what is estimated vs retrieved.
- Ask clarifying questions only if necessary.
""".strip()


# -------------------------------------------------------------------
# Runtime Context (optional, future-proof)
# -------------------------------------------------------------------

@dataclass
class Context:
    user_id: str | None = None


# -------------------------------------------------------------------
# Agent Construction
# -------------------------------------------------------------------

_model = init_chat_model(
    settings.MODEL_NAME,
    temperature=settings.MODEL_TEMP,
)

_checkpointer = InMemorySaver()

AGENT = create_agent(
    model=_model,
    system_prompt=SYSTEM_PROMPT,
    tools=TRAVEL_TOOLS,
    context_schema=Context,
    checkpointer=_checkpointer,
)
