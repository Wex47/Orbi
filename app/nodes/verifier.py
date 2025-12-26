from __future__ import annotations

from app.infrastructure.llm import get_verifier_model


VERIFIER_SYSTEM = """
You are a verification agent.

Check whether the proposed answer is sensible and consistent with:
- the conversation
- the query
- any tool-derived facts (if mentioned)

Rules:
- Do NOT call tools.
- If there are unsupported claims or contradictions, mark INVALID.
- If OK, mark VERIFIED.

Return exactly:
VERIFIED
or
INVALID: <one short reason>
""".strip()


def verifier_node(state: dict) -> dict:
    model = get_verifier_model()

    query = state.get("query") or []
    execution = state.get("execution") or ""

    verifier_prompt = (
        "Verify the following.\n\n"
        f"query:\n{query}\n\n"
        f"Proposed answer:\n{execution}\n"
    )

    messages = (
        [{"role": "system", "content": VERIFIER_SYSTEM}]
        + state["messages"]
        + [{"role": "user", "content": verifier_prompt}]
    )

    verdict = model.invoke(messages).content.strip()
    verified = verdict.startswith("VERIFIED")

    # If invalid, keep the reason for debugging; you can also loop/retry later.
    return {"verified": verified}
