from pydantic import BaseModel
from typing import List


class Plan(BaseModel):
    """
    Structured reasoning output produced by the planner step.
    This is NOT shown to the user.
    """

    user_intent: str
    missing_info: List[str]
    tools_to_use: List[str]
    assumptions: List[str]
