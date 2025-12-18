# from app.agents.agent import AGENT, Context

# def main() -> None:
#     print("Travel Assistant (type 'exit' to quit)\n")

#     config = {"configurable": {"thread_id": "cli-session-1"}}
#     context = Context(user_id="1")

#     while True:
#         user_input = input("You: ").strip()

#         if user_input.lower() in {"exit", "quit"}:
#             print("Goodbye")
#             break

#         response = AGENT.invoke(
#             {"messages": [{"role": "user", "content": user_input}]},
#             config=config,
#             context=context,
#         )

#         # Unified agent returns messages + optional structured output
#         if "structured_response" in response:
#             print("Assistant:", response["structured_response"])
#         else:
#             # Fallback to natural language output
#             print("Assistant:", response["messages"][-1].content)

#         print()


# if __name__ == "__main__":
#     main()


# from app.agents.agent import AGENT, Context
# from app.facts_policy import tools_were_used


# def main() -> None:
#     print("Travel Assistant (type 'exit' to quit)\n")

#     config = {"configurable": {"thread_id": "cli-session-1"}}
#     context = Context(user_id="1")

#     while True:
#         user_input = input("You: ").strip()

#         if user_input.lower() in {"exit", "quit"}:
#             print("Goodbye")
#             break

#         response = AGENT.invoke(
#             {"messages": [{"role": "user", "content": user_input}]},
#             config=config,
#             context=context,
#         )

#         # Unified agent returns messages + optional structured output
#         if "structured_response" in response:
#             print("Assistant:", response["structured_response"])
#         else:
#             print("Assistant:", response["messages"][-1].content)

#         if not tools_were_used(response):
#             print(
#                 "***Note: This answer is based on knowledge of the LLM, "
#                 "not retrieved data from tools.***"
#             )

#         print()


# if __name__ == "__main__":
#     main()


from __future__ import annotations

import os
import uuid
from dotenv import load_dotenv

from app.graph import build_graph

load_dotenv()


def main():
    graph = build_graph()

    # One thread per conversation session. Reuse this value to keep memory.
    thread_id = os.getenv("THREAD_ID") or str(uuid.uuid4())
    print(f"[thread_id={thread_id}] (set THREAD_ID env var to resume)")

    while True:
        text = input("\nYou: ").strip()
        if not text:
            continue
        if text.lower() in {"exit", "quit"}:
            break

        # Provide the user message as an appended message.
        result = graph.invoke(
            {"messages": [{"role": "user", "content": text}]},
            config={"configurable": {"thread_id": thread_id}},
        )

        print("\nAgent:", result["final_answer"])


if __name__ == "__main__":
    main()
