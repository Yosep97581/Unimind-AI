import ollama


def check_ollama_connection():
    try:
        response = ollama.list()
        model_count = len(response.models)

        return (
            True,
            f"Ollama is running. {model_count} local model(s) found."
        )

    except Exception as error:
        return (
            False,
            f"Ollama is not reachable: {error}"
        )


def ask_model(model, question, retrieved_chunks):
    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"""
SOURCE:
Document: {chunk['document_name']}
Page: {chunk['page_number']}

CONTENT:
{chunk['text']}
"""
        )

    context = "\n".join(context_parts)

    system_prompt = """
You are UniMind AI, a university study assistant.

Answer using only the provided retrieved context.

Rules:
1. Do not use outside knowledge.
2. If the context is insufficient, say that clearly.
3. Do not invent page numbers.
4. Explain difficult ideas simply.
5. Keep the answer relevant to the student's question.
"""

    user_prompt = f"""
RETRIEVED CONTEXT:

{context}

QUESTION:

{question}
"""

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        options={
            "temperature": 0.2,
        },
    )

    return response.message.content