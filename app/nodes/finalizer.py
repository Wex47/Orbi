from __future__ import annotations


def finalizer_node(state: dict) -> dict:
    execution = state.get("execution") or ""
    verified = bool(state.get("verified"))

    if verified:
        final = execution
    else:
        final = (
            "I’m not fully confident the result is correct.\n"
            "Could you clarify what you mean and be specific?"
        )

    # Append assistant message to conversation memory
    return {
        "final_answer": final,
        "messages": [{"role": "assistant", "content": final}],
    }
