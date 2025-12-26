from __future__ import annotations

from app.infrastructure.llm import get_lightweight_chat_model


# ROUTER_SYSTEM = """
# You are a routing component for a travel assistant.

# Decide whether the user's message requires:
# - factual information / or multi-step work (PLAN)
# or
# - a direct conversational answer (DIRECT)

# Speical rules:
# - Determine if the query is related to travel. if not - go with DIRECT.
# - if you are unsure which path to take, go with PLAN.

# Return ONLY one word: PLAN or DIRECT.
# """.strip()


# def router_node(state: dict) -> dict:
#     model = get_chat_model()
#     messages = [{"role": "system", "content": ROUTER_SYSTEM}] + state["messages"]
#     out = model.invoke(messages).content.strip().upper()

#     route = "PLAN" if out.startswith("PLAN") else "DIRECT"
#     return {"route": route}


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


def router_node(state: dict) -> dict:
    model = get_lightweight_chat_model()

    last_message = state["messages"][-1]
    if isinstance(last_message, dict):
        query = last_message.get("content", "")
    else:
        query = getattr(last_message, "content", "")

    messages = [{"role": "system", "content": ROUTER_SYSTEM}] + state["messages"]
    out = model.invoke(messages).content.strip().upper()

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


# def router_node(state: dict) -> dict:
#     model = get_lightweight_chat_model()
#     state["query"] = state["messages"][-1]
#     messages = [{"role": "system", "content": ROUTER_SYSTEM}] + state["messages"]

#     out = model.invoke(messages).content.strip().upper()

#     if out.startswith("OFF_TOPIC"):
#         route = "OFF_TOPIC"
#     elif out.startswith("PLAN"):
#         route = "PLAN"
#     elif out.startswith("DIRECT"):
#         route = "DIRECT"
#     else:
#         # Defensive fallback: prefer safety over under-handling
#         route = "PLAN"

#     return {"route": route}

