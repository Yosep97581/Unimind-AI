from io import BytesIO

import pymupdf


def extract_pdf_pages(pdf_bytes: bytes) -> list[dict]:
    """Extract readable text from every page of a PDF.

    Returns:
        A list such as:
        [
            {"page_number": 1, "text": "..."},
            {"page_number": 2, "text": "..."},
        ]
    """
    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    document = pymupdf.open(stream=BytesIO(pdf_bytes), filetype="pdf")
    pages: list[dict] = []

    for index, page in enumerate(document):
        text = page.get_text("text", sort=True).strip()

        if text:
            pages.append(
                {
                    "page_number": index + 1,
                    "text": text,
                }
            )

    document.close()

    if not pages:
        raise ValueError(
            "No selectable text was found. This starter version does not yet "
            "support scanned/image-only PDFs."
        )

    return pages
