from __future__ import annotations

import os
import uuid
from dotenv import load_dotenv

from app.graph import build_graph

load_dotenv()


def main():
    graph = build_graph()

    # added for debugging
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open("langgraph.png", "wb") as f:
        f.write(png_bytes)


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

        print()  # newline after full response


if __name__ == "__main__":
    main()

# assuming you have: graph = StateGraph(...).compile()

