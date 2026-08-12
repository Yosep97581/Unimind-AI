from typing import Any

import ollama


MAX_CONTEXT_CHARACTERS = 24_000


def check_ollama_connection() -> tuple[bool, str]:
    """Check whether the local Ollama service can be reached."""
    try:
        response: Any = ollama.list()
        model_count = len(response.models)
        return True, f"Ollama is running. {model_count} local model(s) found."
    except Exception as error:
        return False, f"Ollama is not reachable: {error}"


def build_document_context(pages: list[dict]) -> str:
    """Build a page-labelled context for the Week 1 starter version.

    The text is intentionally capped. In the next project stage, retrieval
    will replace this full-document approach.
    """
    sections: list[str] = []
    used_characters = 0

    for page in pages:
        section = (
            f"\n--- PAGE {page['page_number']} ---\n"
            f"{page['text']}\n"
        )

        remaining = MAX_CONTEXT_CHARACTERS - used_characters
        if remaining <= 0:
            break

        sections.append(section[:remaining])
        used_characters += min(len(section), remaining)

    return "".join(sections)


def ask_model(model: str, question: str, pages: list[dict]) -> str:
    """Ask Ollama to answer only from the uploaded PDF context."""
    context = build_document_context(pages)

    system_prompt = """
You are UniMind AI, a careful university study assistant.

Rules:
1. Answer using only the supplied PDF context.
2. If the context does not contain enough information, say so clearly.
3. Do not invent facts, formulas, quotations, or page references.
4. Explain difficult ideas in simple language.
5. End with a short 'Sources' line listing the relevant PDF page number(s).
""".strip()

    user_prompt = f"""
PDF CONTEXT:
{context}

QUESTION:
{question}
""".strip()

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={
            "temperature": 0.2,
        },
    )

    return response.message.content
