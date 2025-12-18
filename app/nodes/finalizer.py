from __future__ import annotations


# def finalizer_node(state: dict) -> dict:
#     execution = state.get("execution") or ""
#     verified = bool(state.get("verified"))

#     if verified:
#         final = execution
#     else:
#         final = (
#             "I’m not fully confident the result is correct.\n"
#             "Could you clarify what you mean and be specific?"
#         )

#     # Append assistant message to conversation memory
#     return {
#         "final_answer": final,
#         "messages": [{"role": "assistant", "content": final}],
#     }


def finalizer_node(state: dict) -> dict:
    execution = state.get("execution") or ""
    verified = bool(state.get("verified"))
    tools_used = bool(state.get("tools_used"))
    route = state.get("route")

    warnings: list[str] = []

    if not verified:
        warnings.append(
            "***This answer could not be fully verified for correctness.***"
        )

    if not tools_used or route == "DIRECT":
        warnings.append(
            "***This answer is based on the LLM Knowledge and was not grounded in tool invocation.***"
        )

    if warnings:
        warning_block = "\n".join(warnings)
        final_answer = f"{execution}\n\n---\n{warning_block}"
    else:
        final_answer = execution

    return {
        "final_answer": final_answer,
        # Append to conversation memory
        "messages": [{"role": "assistant", "content": final_answer}],
    }
