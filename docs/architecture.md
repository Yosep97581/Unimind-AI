User uploads PDFs
    ↓
PyMuPDF extracts page text
    ↓
Text is split into overlapping chunks
    ↓
EmbeddingGemma generates embeddings
    ↓
ChromaDB stores:
    - text
    - embedding
    - document name
    - page number
    - chunk id
    ↓
User asks question
    ↓
Question embedding generated
    ↓
ChromaDB similarity search
    ↓
Distance threshold filters weak matches
    ↓
Relevant chunks sent to Gemma 3 4B
    ↓
Study tool generates answer
    ↓
Streamlit displays answer + source metadata