from app.infrastructure.llm import get_verifier_model

verifier = get_verifier_model()

response = verifier.invoke(
    "Answer with YES or NO only. Is Paris the capital of France?"
)

print(response.content)