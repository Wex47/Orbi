from __future__ import annotations

from app.config.settings import settings

DIRECT_SYSTEM = """
You are a professional travel assistant.
Answer conversationally and helpfully.

Special rule:
- If the query is not related to travel, let them know you cannot provide off-topic responses.

""".strip()


def direct_node(state: dict) -> dict:
    model = settings.get_chat_model()
    messages = [{"role": "system", "content": DIRECT_SYSTEM}] + state["messages"]
    answer = model.invoke(messages).content

    return {
        "execution": answer,
        "verified": True,  # direct path doesn't run verification in this simple setup
    }
