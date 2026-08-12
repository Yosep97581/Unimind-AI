import chromadb


CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "unimind_documents"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def store_chunks(chunks, embeddings, document_name):
    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(
            f"{document_name}-{chunk['id']}"
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            {
                "document_name": document_name,
                "page_number": chunk["page_number"],
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search_chunks(query_embedding, n_results=4):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    return results