from __future__ import annotations

from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langmem.short_term import RunningSummary

"""
Defines the state structure used throughout the graph nodes.
"""

class State(TypedDict):
    # Conversational memory (appended, not overwritten)
    messages: Annotated[list, add_messages]

    # used by the summarizer node
    context: dict[str, RunningSummary]

    # Routing + workflow artifacts
    route: Optional[Literal["DIRECT", "PLAN", "OFF_TOPIC"]]

    query: Optional[str]
    execution: Optional[str]
    tools_used: bool
    verified: Optional[bool]
    final_answer: Optional[str]
