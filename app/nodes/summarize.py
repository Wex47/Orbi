from langmem.short_term import SummarizationNode
from langchain_core.messages.utils import count_tokens_approximately
from app.infrastructure.llm import get_chat_model
from app.config.settings import settings


def build_summarization_node() -> SummarizationNode:
    """
    Builds a summarization node for short-term memory control.
    
    - Summarizes only when thresholds are crossed
    - Keeps summary size bounded
    - Safe to run on every graph iteration
    """
    base_model = get_chat_model()

    summarization_model = base_model.bind(max_tokens=settings.MAX_SUMMARY_OUTPUT_TOKENS)

    return SummarizationNode(
        token_counter=count_tokens_approximately,

        model=summarization_model,

        # Hard upper bound for model input
        max_tokens=settings.MAX_SUMMARY_INPUT_TOKENS,

        # Summary is triggered ONLY above this
        max_tokens_before_summary=settings.SUMMARY_TOKENS_THRESHOLD,

        # Prevent summary re-explosion
        max_summary_tokens=settings.MAX_SUMMARY_OUTPUT_TOKENS,

        input_messages_key="messages",
        output_messages_key="messages",
    )
