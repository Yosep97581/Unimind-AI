# UniMind AI

UniMind AI is a local study assistant that answers questions about uploaded
university PDFs using a locally running Ollama model.

## Current milestone

This starter version demonstrates the complete basic path:

1. Upload one text-based PDF.
2. Extract text while retaining page numbers.
3. Send the PDF context and question to a local language model.
4. Display the answer in a Streamlit chat interface.

This is intentionally **not yet full RAG**. The next milestone will add text
chunking, embeddings, ChromaDB retrieval, stronger source handling, and tests.

## Requirements

- Windows 10/11
- Python 3.11 or 3.12 recommended
- Ollama
- VS Code

## Setup

### 1. Install and test Ollama

Install Ollama for Windows, then open PowerShell:

```powershell
ollama pull gemma3:4b
ollama run gemma3:4b
```

Ask it a simple question. Enter `/bye` to exit.

### 2. Open this folder in VS Code

Open a terminal in the project root.

### 3. Create a virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Python 3.12 is unavailable:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the application

```powershell
streamlit run app.py
```

Streamlit should open the application in your browser.

## Known limitations

- Only one PDF is supported.
- Scanned/image-only PDFs are not supported.
- The starter sends only a limited amount of document text to the model.
- Page citations are model-generated and are not yet programmatically verified.
- There is no vector database or semantic retrieval yet.

## Planned architecture

```text
PDF
  -> extraction with page metadata
  -> chunking
  -> embedding generation
  -> ChromaDB storage

Question
  -> question embedding
  -> similarity search
  -> relevant chunks
  -> local LLM
  -> answer with verified sources
```

## Why the repository is structured this way

`app.py` contains only the interface and application flow. PDF handling and
model communication are separated into `src/` modules so each component can
later be tested and replaced independently.
