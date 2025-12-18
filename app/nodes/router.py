from __future__ import annotations

from app.infrastructure.llm import get_chat_model


ROUTER_SYSTEM = """
You are a routing component for a travel assistant.

Decide whether the user's message requires:
- factual information / or multi-step work (PLAN)
or
- a direct conversational answer (DIRECT)

Speical rules:
- Determine if the query is related to travel. if not - go with DIRECT.
- if you are unsure which path to take, go with PLAN.

Return ONLY one word: PLAN or DIRECT.
""".strip()


def router_node(state: dict) -> dict:
    model = get_chat_model()
    messages = [{"role": "system", "content": ROUTER_SYSTEM}] + state["messages"]
    out = model.invoke(messages).content.strip().upper()

    route = "PLAN" if out.startswith("PLAN") else "DIRECT"
    return {"route": route}
