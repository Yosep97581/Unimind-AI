# UniMind AI

UniMind AI is a local AI-powered study assistant designed to help students interact with university learning materials using Retrieval-Augmented Generation (RAG).

Users can upload multiple PDF documents, ask questions about their contents, generate summaries, create flashcards and practice questions, compare concepts, and receive responses grounded in the uploaded materials.

The entire AI pipeline can run locally using Ollama, allowing the application to work without relying on paid cloud LLM APIs.

## Features

* Local LLM inference using Ollama
* Multi-PDF document support
* Persistent document knowledge base
* Retrieval-Augmented Generation (RAG)
* Semantic search using vector embeddings
* ChromaDB vector storage
* Source-aware responses with document and page references
* Relevance filtering for weak retrieval matches
* Summary generation
* Practice-question generation
* Flashcard generation
* Concept and document comparison
* Automatic study-tool intent routing
* Manual study-mode selection
* Short-term conversational memory
* Persistent document metadata
* Document deletion
* Local-first architecture

## Tech Stack

### Core

* Python
* Streamlit
* Ollama
* Gemma 3
* EmbeddingGemma

### Document Processing

* PyMuPDF

### Retrieval

* ChromaDB
* Vector embeddings
* Semantic similarity search
* Metadata filtering

### Testing

* pytest

## Architecture

UniMind processes documents through a local RAG pipeline.

```text
PDF Upload
    ↓
PyMuPDF
    ↓
Page-level text extraction
    ↓
Text chunking with overlap
    ↓
EmbeddingGemma
    ↓
Vector embeddings
    ↓
ChromaDB
    ↓
Persistent knowledge base


User Question
    ↓
EmbeddingGemma
    ↓
Query embedding
    ↓
ChromaDB similarity search
    ↓
Top matching chunks
    ↓
Relevance threshold
    ↓
Relevant context
    ↓
Study tool / intent router
    ↓
Gemma 3
    ↓
Grounded response
    ↓
Source metadata
```

The application stores document name, page number and chunk identifiers alongside each vector so retrieved answers can be associated with their original sources.

More architecture information is available in:

```text
docs/architecture.md
```

## How RAG Works

Instead of sending an entire PDF directly to the language model, UniMind first searches for the parts of the uploaded documents that are most relevant to the user's question.

For example, if a student asks:

> How is expected value calculated?

UniMind performs the following process:

1. Converts the question into an embedding.
2. Searches ChromaDB for semantically similar document chunks.
3. Filters weak matches using a retrieval-distance threshold.
4. Sends only the relevant chunks to the language model.
5. Generates an answer based on the retrieved material.
6. Displays the corresponding document and page sources.

This allows UniMind to work with larger document collections while reducing irrelevant context and hallucination risk.

## Study Tools

UniMind supports several study modes.

### Auto

Automatically determines the most appropriate study tool based on the user's request.

Example:

```text
Summarise the probability section.
```

UniMind routes the request to the summarisation tool.

### Question Answering

Answers questions using retrieved university material.

Example:

```text
How is expected value calculated?
```

### Summary

Produces study-friendly summaries from retrieved material.

Example:

```text
Summarise the main concepts about probability.
```

### Practice Questions

Generates practice questions based only on uploaded learning material.

Example:

```text
Create five practice questions about expected value.
```

### Flashcards

Creates question-and-answer flashcards.

Example:

```text
Create flashcards about normal distributions.
```

### Compare

Compares concepts or material found across uploaded documents.

Example:

```text
Compare expected value and variance.
```

## Conversation Memory

UniMind maintains short-term conversation history during the current Streamlit session.

This allows follow-up interactions such as:

```text
User:
What is the cancer screening problem about?

User:
Why is that important?
```

The second question can use the previous conversation to understand what "that" refers to.

Conversation history is used for contextual understanding only. Retrieved university material remains the source of factual information.

## Persistent Knowledge Base

Uploaded documents are processed into vector embeddings and stored locally in ChromaDB.

Document names are also stored in:

```text
data/documents.json
```

This means the document collection can remain available after restarting the Streamlit application without requiring every PDF to be embedded again.

Users can also remove documents from the application. Deleting a document removes:

* its metadata entry
* its vector chunks from ChromaDB
* its entry from the current Streamlit session

## Retrieval Relevance Filtering

Early testing showed that ChromaDB always returns the nearest available chunks even when a question is unrelated to the uploaded material.

For example, an unrelated question such as:

```text
What is JavaScript?
```

still returned mathematics chunks because they were technically the closest available vectors.

To reduce irrelevant retrieval, UniMind applies a maximum distance threshold before context is sent to the language model.

During initial testing:

```text
Relevant retrieval distances:
approximately 1.23–1.38

Irrelevant retrieval distances:
approximately 1.64–1.81
```

A provisional threshold of:

```text
1.45
```

was selected based on these observations.

Further details are available in:

```text
docs/evaluation.md
```

## Project Structure

```text
Unimind-AI/
│
├── app.py
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
│
├── data/
│   ├── documents.json
│   ├── uploads/
│   └── chroma_db/
│
├── docs/
│   ├── architecture.md
│   ├── evaluation.md
│   └── project_plan.md
│
├── screenshots/
│
├── tests/
│   ├── test_intent_router.py
│   └── test_text_splitter.py
│
└── src/
    ├── __init__.py
    ├── document_store.py
    ├── embeddings.py
    ├── intent_router.py
    ├── llm_client.py
    ├── memory.py
    ├── pdf_loader.py
    ├── rag_pipeline.py
    ├── study_tools.py
    ├── text_splitter.py
    └── vector_store.py
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Unimind-AI
```

### 2. Create a virtual environment

On Linux or WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Follow the official Ollama installation instructions for your operating system.

On Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 5. Download the language model

```bash
ollama pull gemma3:4b
```

### 6. Download the embedding model

```bash
ollama pull embeddinggemma
```

Check installed models:

```bash
ollama list
```

You should see both models.

### 7. Verify Ollama

```bash
curl http://localhost:11434
```

Expected response:

```text
Ollama is running
```

### 8. Start UniMind

```bash
python -m streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

Usually:

```text
http://localhost:8501
```

## Usage

1. Start Ollama.
2. Launch the Streamlit application.
3. Upload one or more text-based PDF documents.
4. Wait for document processing to complete.
5. Select a study mode or leave the mode on Auto.
6. Ask questions about the uploaded material.
7. Review the answer and retrieved sources.
8. Delete documents from the sidebar when they are no longer needed.

## Running Tests

Install pytest if necessary:

```bash
pip install pytest
```

Run:

```bash
pytest
```

or:

```bash
python -m pytest
```

The current test suite includes basic validation for:

* intent routing
* text chunk creation
* default question routing
* flashcard routing
* summary routing

Additional integration and retrieval tests are planned.

## Example

Uploaded material:

```text
M1 T1 Tutorial.pdf
Probability Lecture.pdf
Practice Questions.pdf
```

Question:

```text
How is expected value calculated?
```

UniMind:

1. embeds the question
2. searches the vector database
3. retrieves relevant chunks
4. filters weak matches
5. sends the remaining context to the local model
6. returns an explanation
7. displays the source document and page

## Privacy

UniMind is designed as a local-first application.

When using locally installed Ollama models, document processing, embeddings and LLM inference can remain on the user's machine.

The application does not require an OpenAI, Anthropic or Gemini API key for its core functionality.

## Current Limitations

* Scanned or image-only PDFs are not currently supported.
* PDF identity is currently based primarily on filename.
* Two unrelated files with the same filename may be treated as the same document.
* Chat history is session-based and is not currently persisted after restart.
* The retrieval threshold was tuned using a relatively small evaluation set.
* Chunking is currently character-based rather than fully semantic.
* There is no authentication or multi-user support.
* There is no cloud deployment in the current version.
* Some complex PDF formatting may not extract cleanly.
* Study-tool output quality depends on the selected local language model.

## Future Improvements

Potential future improvements include:

* SHA-256 document hashing
* OCR support for scanned PDFs
* semantic or sentence-aware chunking
* persistent chat history
* document-specific search filters
* course or folder organisation
* configurable embedding models
* configurable generation models
* query rewriting
* reranking retrieved chunks
* larger RAG evaluation dataset
* retrieval evaluation dashboard
* flashcard export
* quiz scoring
* spaced-repetition features
* user accounts
* packaged desktop version

## Development Journey

UniMind was developed incrementally across five milestones.

### Milestone 1 — Local PDF Chat

Built the initial Streamlit interface and connected a local Ollama model to extracted PDF text.

### Milestone 2 — RAG Pipeline

Added:

* text chunking
* embeddings
* ChromaDB
* semantic retrieval
* page metadata
* relevance filtering

### Milestone 3 — Persistent Multi-Document Knowledge Base

Added:

* multiple PDF upload
* persistent document metadata
* cross-document retrieval
* duplicate prevention
* document deletion

### Milestone 4 — Study Agent Features

Added:

* summaries
* practice questions
* flashcards
* concept comparison
* intent routing
* manual study modes
* short-term conversation memory

### Milestone 5 — Portfolio and Engineering Polish

Added:

* automated tests
* project documentation
* architecture documentation
* retrieval evaluation
* UI cleanup
* portfolio presentation

## What I Learned

This project was built to explore both AI development and practical software engineering.

Key areas developed through the project include:

* Retrieval-Augmented Generation
* vector databases
* local LLM inference
* embedding models
* semantic similarity search
* prompt design
* document processing
* application state management
* persistent local storage
* modular Python architecture
* testing
* evaluation of retrieval quality
* debugging AI pipelines

A major focus of the project was understanding each stage of the RAG pipeline rather than relying entirely on high-level frameworks.

## License

This project is currently intended for educational and portfolio purposes.
