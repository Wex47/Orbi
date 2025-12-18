from __future__ import annotations

from app.config.settings import settings


ROUTER_SYSTEM = """
You are a routing component for a travel assistant.

Decide whether the user's message requires:
- factual information / or multi-step work (PLAN)
or
- a direct conversational answer (DIRECT)

if you are unsure, go with PLAN.

Return ONLY one word: PLAN or DIRECT.
""".strip()


def router_node(state: dict) -> dict:
    model = settings.get_chat_model()
    messages = [{"role": "system", "content": ROUTER_SYSTEM}] + state["messages"]
    out = model.invoke(messages).content.strip().upper()

    route = "PLAN" if out.startswith("PLAN") else "DIRECT"
    return {"route": route}
