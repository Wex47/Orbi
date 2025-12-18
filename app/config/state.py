from __future__ import annotations

from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    # Conversational memory (appended, not overwritten)
    messages: Annotated[list, add_messages]

    # Routing + workflow artifacts
    route: Optional[Literal["DIRECT", "PLAN"]]
    plan: Optional[list[str]]
    execution: Optional[str]
    tools_used: bool
    verified: Optional[bool]
    final_answer: Optional[str]
