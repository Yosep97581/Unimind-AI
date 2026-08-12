from src.embeddings import create_embedding
from src.vector_store import search_chunks


MAX_DISTANCE = 1.45


def retrieve_context(question, n_results=4):
    query_embedding = create_embedding(question)

    results = search_chunks(
        query_embedding,
        n_results=n_results
    )

    retrieved_chunks = []

    if not results["documents"]:
        return retrieved_chunks

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        if distance <= MAX_DISTANCE:
            retrieved_chunks.append(
                {
                    "text": document,
                    "document_name": metadata["document_name"],
                    "page_number": metadata["page_number"],
                    "distance": distance,
                }
            )

    return retrieved_chunks