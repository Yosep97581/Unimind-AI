from src.text_splitter import split_pages_into_chunks


def test_chunk_creation():
    pages = [
        {
            "page_number": 1,
            "text": "A" * 2500
        }
    ]

    chunks = split_pages_into_chunks(
        pages,
        chunk_size=1000,
        overlap=150
    )

    assert len(chunks) > 1
    assert chunks[0]["page_number"] == 1