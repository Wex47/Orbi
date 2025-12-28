from __future__ import annotations
from typing import Dict, Any
from app.infrastructure.llm import get_verifier_model
from app.infrastructure.llm import get_lightweight_chat_model
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

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


def verifier_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    validates the correctness of the proposed answer based on consistency and sensibility.
    inputs: 'query', 'execution', 'messages'
    outputs: 'verified' (bool)
    """
    # model = get_verifier_model()
    model = get_lightweight_chat_model()

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

    try:
        verdict = model.invoke(messages).content.strip()
        logger.debug(settings.SUCCESS_GENERIC)
    except Exception as exc:
        logger.exception(settings.FAILED_GENERIC)
        raise exc
    
    verified = verdict.startswith("VERIFIED")

    return {"verified": verified}