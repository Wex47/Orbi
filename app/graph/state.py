from __future__ import annotations

from typing import Annotated, Literal, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langmem.short_term import RunningSummary

class State(TypedDict, total=False):
    # Conversational memory (append-only)
    messages: Annotated[list[Any], add_messages]

    # Summarization context
    context: dict[str, RunningSummary]

    # Routing
    route: Literal["DIRECT", "PLAN", "OFF_TOPIC"]
    query: str

    # Execution
    execution: str
    tools_used: bool

    # Verification
    verified: bool

    # Final output
    final_answer: str