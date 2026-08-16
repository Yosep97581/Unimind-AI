from src.intent_router import detect_intent


def test_summary_intent():
    assert detect_intent(
        "Summarise this topic"
    ) == "summary"


def test_flashcard_intent():
    assert detect_intent(
        "Make flashcards about probability"
    ) == "flashcards"


def test_default_question_intent():
    assert detect_intent(
        "What is expected value?"
    ) == "question"