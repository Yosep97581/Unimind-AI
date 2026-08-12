def split_pages_into_chunks(
    pages,
    chunk_size=1000,
    overlap=150
):
    chunks = []

    chunk_id = 0

    for page in pages:
        text = page["text"]
        page_number = page["page_number"]

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append(
                    {
                        "id": f"chunk-{chunk_id}",
                        "text": chunk_text.strip(),
                        "page_number": page_number,
                    }
                )

                chunk_id += 1

            start += chunk_size - overlap

    return chunks

#Temporary

if __name__ == "__main__":
    fake_pages = [
        {
            "page_number": 1,
            "text": "A" * 2500
        }
    ]

    chunks = split_pages_into_chunks(fake_pages)

    for chunk in chunks:
        print(chunk["id"])
        print(chunk["page_number"])
        print(len(chunk["text"]))
        print()