from __future__ import annotations

from app.config.settings import settings


DIRECT_SYSTEM = """
You are a professional travel assistant.
Answer conversationally and helpfully.
If the user asks for real-world facts you don't have, suggest using tools next time.
""".strip()


def direct_node(state: dict) -> dict:
    model = settings.get_chat_model()
    messages = [{"role": "system", "content": DIRECT_SYSTEM}] + state["messages"]
    answer = model.invoke(messages).content

    return {
        "execution": answer,
        "verified": True,  # direct path doesn't run verification in this simple setup
    }
