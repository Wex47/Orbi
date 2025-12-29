from __future__ import annotations
import uuid
from langgraph.checkpoint.postgres import PostgresSaver
from app.config.settings import settings
from app.graph.graph import build_graph
from app.config.logger import setup_logging


def main():

    # SETUP
    setup_logging()
    thread_id = settings.THREAD_ID or str(uuid.uuid4()) # if not set, generate a uuid
    #

    with PostgresSaver.from_conn_string(settings.postgres_dsn) as checkpointer:

        checkpointer.setup() # create the tables if they dont exist
        graph = build_graph(checkpointer)

        print("Welcome to Orbi! Type 'exit' or 'quit' to leave.")
        print(f"[thread_id={thread_id}]")

        while True:
            text = input("\nYou: ").strip()
            if not text:
                continue
            if text.lower() in {"exit", "quit"}:
                break

            result = graph.invoke(
                {"messages": [{"role": "user", "content": text}]},
                config={"configurable": {"thread_id": thread_id}},
            )

            print("\nAgent:", result["final_answer"])


if __name__ == "__main__":
    main()