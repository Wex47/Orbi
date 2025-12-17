from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from app.config.settings import settings
from app.planner.plan import Plan


PLANNER_PROMPT = """
You are a planning module for a travel assistant.

Given the conversation so far and the user's latest request:

1. Identify the user's intent.
2. Determine what information is required to answer reliably.
3. Decide which tools should be used (by tool name).
4. If required information is missing or ambiguous, list it in missing_info.
5. Do NOT guess facts. If something is unclear, mark it as missing.

Return ONLY valid JSON matching this schema:
{
  "user_intent": string,
  "missing_info": [string],
  "tools_to_use": [string],
  "assumptions": [string]
}
""".strip()


# Deterministic model for planning (important)
_planner_model = init_chat_model(
    settings.MODEL_NAME,
    temperature=0.0,
)


def run_planner(conversation_messages) -> Plan:
    """
    Runs the planning step over the current conversation history
    and returns a structured Plan object.
    """

    messages = [
        SystemMessage(content=PLANNER_PROMPT),
        *conversation_messages,
    ]

    response = _planner_model.invoke(messages)

    return Plan.model_validate_json(response.content)
