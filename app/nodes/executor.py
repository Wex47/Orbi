from __future__ import annotations

from langchain.agents import create_agent

from app.config.settings import settings
from app.tools.tools import TRAVEL_TOOLS


EXECUTOR_SYSTEM = """
You are an execution agent for a travel assistant.

You will be given:
- the conversation so far (messages)
- a plan (list of steps)

Execute the plan in order.
Use tools when needed for factual data.
Be explicit about what came from tools vs what is reasoning.
When you finish, write a complete, engaging user-facing answer.

Do not show the plan unless the user asked for it.
""".strip()


# We create a single tool-calling agent instance.
# In LangChain v1, create_agent is the standard way to build agents. :contentReference[oaicite:4]{index=4}
_AGENT = create_agent(
    model= settings.get_chat_model(),
    tools=TRAVEL_TOOLS,
    system_prompt=EXECUTOR_SYSTEM,
)


def executor_node(state: dict) -> dict:
    plan = state.get("plan") or []
    plan_block = "\n".join(str(x) for x in plan)

    # We add the plan as context in a final user message for the executor.
    exec_input = (
        "Execute the task for the user.\n\n"
        f"Plan:\n{plan_block}\n"
    )

    result = _AGENT.invoke(
        {
            "messages": state["messages"] + [{"role": "user", "content": exec_input}]
        }
    )

    # create_agent returns a dict; the final assistant message is usually at the end of messages
    # Keep it robust: extract last message content if present.
    messages = result.get("messages", [])
    final_text = ""
    if messages:
        last = messages[-1]
        final_text = last.get("content", "") if isinstance(last, dict) else getattr(last, "content", "")

    return {"execution": final_text}
