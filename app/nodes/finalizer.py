from __future__ import annotations
from typing import Dict, Any

def finalizer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Finalizer node that appends warnings to the final answer
    based on verification status and tool usage.

    inputs: 'execution', 'verified' (bool), 'tools_used' (bool), 'route'
    outputs: 'final_answer', 'messages'
    """
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
        "messages": [{"role": "assistant", "content": final_answer}], # Append to conversation memory
    }
