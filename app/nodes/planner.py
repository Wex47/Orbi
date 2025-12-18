from __future__ import annotations
from app.infrastructure.llm import get_chat_model


PLANNER_SYSTEM = """
You are a planning agent.

Given the conversation so far, produce a short step-by-step plan.
Rules:
- Output 3 to 8 steps.
- Mark steps that need external data with: [TOOL]
- Do NOT name specific tool functions.
- Do NOT execute anything.
Return as a numbered list.
""".strip()


def _parse_numbered_list(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        # keep it simple; accept "1." / "- " / etc.
        if s[0].isdigit():
            lines.append(s)
        else:
            lines.append(s)
    return lines[:8]


def planner_node(state: dict) -> dict:
    model = get_chat_model()
    messages = [{"role": "system", "content": PLANNER_SYSTEM}] + state["messages"]
    plan_text = model.invoke(messages).content
    plan = _parse_numbered_list(plan_text)

    return {"plan": plan}
