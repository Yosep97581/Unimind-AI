import ollama


def build_context(retrieved_chunks):
    parts = []

    for chunk in retrieved_chunks:
        parts.append(
            f"""
Document: {chunk['document_name']}
Page: {chunk['page_number']}

{chunk['text']}
"""
        )

    return "\n".join(parts)


def answer_question(
    model,
    question,
    retrieved_chunks,
    history=None
):
    context = build_context(
        retrieved_chunks
    )

    messages = [
        {
            "role": "system",
            "content": """
You are UniMind AI, a university study assistant.

Rules:
1. Answer using only the retrieved university material.
2. Use conversation history only to understand references
   such as "that question", "it", "the previous one",
   or "what you just explained".
3. Do not treat conversation history as a factual source.
4. If the retrieved material does not contain enough information,
   say so clearly.
5. Explain difficult concepts simply.
"""
        }
    ]

    if history:
        messages.extend(
            history
        )

    messages.append(
        {
            "role": "user",
            "content": f"""
RETRIEVED CONTEXT:

{context}

CURRENT QUESTION:

{question}
"""
        }
    )

    response = ollama.chat(
        model=model,
        messages=messages,
        options={
            "temperature": 0.2
        },
    )

    return response.message.content

def summarise_material(
    model,
    retrieved_chunks
):
    context = build_context(retrieved_chunks)

    prompt = f"""
You are UniMind AI, a university study assistant.

Summarise the provided university material.

Use only the provided context.

Requirements:
- identify the main topics
- explain the key concepts clearly
- include important formulas if present
- organise the summary so it is easy to study
- do not invent information that is not in the context

CONTEXT:

{context}
"""

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={
            "temperature": 0.2
        },
    )

    return response.message.content

def generate_practice_questions(
    model,
    retrieved_chunks,
    number_of_questions=5
):
    context = build_context(retrieved_chunks)

    prompt = f"""
You are UniMind AI.

Create {number_of_questions} practice questions
using only the provided university material.

Requirements:
- vary the difficulty
- do not provide answers immediately
- cover important concepts
- avoid questions unrelated to the context

CONTEXT:
{context}
"""

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={"temperature": 0.5},
    )

    return response.message.content

def generate_flashcards(
    model,
    retrieved_chunks,
    number_of_cards=8
):
    context = build_context(retrieved_chunks)

    prompt = f"""
Create {number_of_cards} study flashcards
from the provided material.

Format each flashcard like:

Q: ...
A: ...

Requirements:
- keep questions concise
- answers should be clear
- focus on important concepts
- use only the provided context

CONTEXT:
{context}
"""

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={"temperature": 0.4},
    )

    return response.message.content

def compare_material(model, question, retrieved_chunks):
    context = build_context(retrieved_chunks)

    prompt = f"""
You are UniMind AI.

Compare the concepts or documents requested by the student.

Use only the provided context.

CONTEXT:
{context}

REQUEST:
{question}

Clearly show:
- similarities
- differences
- important relationships
- which document each point comes from where possible
"""

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={"temperature": 0.2},
    )

    return response.message.content