import json
from pathlib import Path


DOCUMENT_FILE = Path("data/documents.json")


def load_documents():
    if not DOCUMENT_FILE.exists():
        return []

    try:
        with open(
            DOCUMENT_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            content = file.read().strip()

            if not content:
                return []

            return json.loads(content)

    except json.JSONDecodeError:
        return []


def save_documents(documents):
    DOCUMENT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        DOCUMENT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            documents,
            file,
            indent=2
        )


def add_document(document_name):
    documents = load_documents()

    if document_name not in documents:
        documents.append(document_name)

        save_documents(documents)
        
def remove_document(document_name):
    documents = load_documents()

    if document_name in documents:
        documents.remove(document_name)
        save_documents(documents)