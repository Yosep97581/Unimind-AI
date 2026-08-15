def detect_intent(question):
    text = question.lower()

    if "summarise" in text or "summarize" in text:
        return "summary"

    if "flashcard" in text:
        return "flashcards"

    if (
        "practice question" in text
        or "quiz me" in text
        or "make questions" in text
    ):
        return "practice"

    if "compare" in text or "difference between" in text:
        return "compare"

    return "question"