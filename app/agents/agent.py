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

# SYSTEM_PROMPT = """
# You are a professional travel planning assistant.

# Rules:
# - Use tools whenever factual data is required.
# - Be explicit about what is estimated vs retrieved.
# - Ask clarifying questions only if necessary.
# """.strip()

SYSTEM_PROMPT = """
You are a professional travel planning assistant.

Before answering any user request, follow this reasoning process:

1. Identify the user’s intent and required information, use conversational history if needed.
2. Decide whether the request requires real-world, factual data.
3. If real-world data is required, use the appropriate tool before answering.
4. If required details are missing or ambiguous, ask a clarifying question.
5. Clearly distinguish between information retrieved from tools and general advice.

Do not guess facts such as prices, availability, weather, or schedules.
Use tools whenever accuracy matters.
"""




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


# Conversation state is persisted on the application side and is re-sent to the LLM on each turn.
_checkpointer = InMemorySaver()



AGENT = create_agent(
    model=_model,
    system_prompt=SYSTEM_PROMPT,
    tools=TRAVEL_TOOLS,
    context_schema=Context,
    checkpointer=_checkpointer,
    debug = True # dev
)
