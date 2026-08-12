import ollama


EMBEDDING_MODEL = "embeddinggemma"


def create_embedding(text):
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response["embeddings"][0]