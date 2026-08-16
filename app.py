import streamlit as st

from src.llm_client import check_ollama_connection
from src.pdf_loader import extract_pdf_pages
from src.text_splitter import split_pages_into_chunks
from src.embeddings import create_embedding
from src.vector_store import (
    store_chunks,
    delete_document,
)
from src.rag_pipeline import retrieve_context
from src.document_store import (
    load_documents,
    add_document,
    remove_document,
)
from src.intent_router import detect_intent
from src.study_tools import (
    answer_question,
    summarise_material,
    generate_practice_questions,
    generate_flashcards,
    compare_material,
)
from src.memory import get_recent_history

st.set_page_config(
    page_title="UniMind AI",
    page_icon="📚",
    layout="wide",
)


# -------------------------------------------------
# SESSION STATE INITIALISATION
# -------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    saved_documents = load_documents()

    st.session_state.documents = {
        name: {}
        for name in saved_documents
    }


# -------------------------------------------------
# PAGE HEADER
# -------------------------------------------------

st.title("📚 UniMind AI")
st.caption(
    "A local AI study assistant for asking questions about university PDFs."
)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:
    st.header("Document")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more text-based PDF files.",
    )

    if st.session_state.documents:
        st.divider()
        st.subheader("Loaded documents")

        for name in list(st.session_state.documents.keys()):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"📄 {name}")

            with col2:
                if st.button(
                    "🗑️",
                    key=f"delete-{name}"
                ):
                    delete_document(name)
                    remove_document(name)

                    del st.session_state.documents[name]

                    st.rerun()

    st.divider()
    st.subheader("Study tools")

    study_mode = st.selectbox(
        "Mode",
        [
            "Auto",
            "Question Answering",
            "Summary",
            "Practice Questions",
            "Flashcards",
            "Compare",
        ]
    )

    st.divider()
    st.header("Local model")

    model_name = st.text_input(
        "Ollama model",
        value="gemma3:4b"
    )

    if st.button(
        "Check Ollama connection",
        use_container_width=True
    ):
        ok, message = check_ollama_connection()

        if ok:
            st.success(message)
        else:
            st.error(message)

if st.sidebar.button(
    "Clear chat",
    use_container_width=True
):
    st.session_state.messages = []
    st.rerun()

if uploaded_files:
    for uploaded_file in uploaded_files:

        if uploaded_file.name not in st.session_state.documents:
            try:
                pages = extract_pdf_pages(
                    uploaded_file.getvalue()
                )

                chunks = split_pages_into_chunks(pages)

                embeddings = []

                for chunk in chunks:
                    embedding = create_embedding(
                        chunk["text"]
                    )

                    embeddings.append(embedding)

                store_chunks(
                    chunks=chunks,
                    embeddings=embeddings,
                    document_name=uploaded_file.name,
                )

                add_document(
                    uploaded_file.name
                )

                st.session_state.documents[
                    uploaded_file.name
                ] = {
                    "pages": pages
                }

                st.success(
                    f"Processed {uploaded_file.name} "
                    f"({len(pages)} pages)"
                )

            except ValueError as error:
                st.error(
                    f"{uploaded_file.name}: {error}"
                )

            except Exception as error:
                st.error(
                    f"Could not process "
                    f"{uploaded_file.name}: {error}"
                )

if st.session_state.documents:
    st.info(
        f"{len(st.session_state.documents)} "
        f"document(s) loaded"
    )

    for document_name in st.session_state.documents:
        st.write(f"- {document_name}")

else:
    st.warning(
        "Upload at least one PDF before asking a question."
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask about your uploaded study materials",
    disabled=not bool(st.session_state.documents),
)

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    history = get_recent_history(
        st.session_state.messages[:-1]
    )
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Reading the document and preparing an answer..."):
            try:
                retrieved_chunks = retrieve_context(
                    question,
                    n_results=4
                )
                
                if study_mode == "Auto":
                    intent = detect_intent(question)

                elif study_mode == "Question Answering":
                    intent = "question"

                elif study_mode == "Summary":
                    intent = "summary"

                elif study_mode == "Practice Questions":
                    intent = "practice"

                elif study_mode == "Flashcards":
                    intent = "flashcards"

                elif study_mode == "Compare":
                    intent = "compare"

                if not retrieved_chunks:
                    answer = (
                        "I couldn't find enough relevant information "
                        "in the uploaded materials."
                    )

                elif intent == "summary":
                    answer = summarise_material(
                        model_name,
                        retrieved_chunks
                    )

                elif intent == "practice":
                    answer = generate_practice_questions(
                        model_name,
                        retrieved_chunks
                    )

                elif intent == "flashcards":
                    answer = generate_flashcards(
                        model_name,
                        retrieved_chunks
                    )

                elif intent == "compare":
                    answer = compare_material(
                        model_name,
                        question,
                        retrieved_chunks
                    )

                else:
                    answer = answer_question(
                        model_name,
                        question,
                        retrieved_chunks,
                        history=history,
                    )

                st.markdown(answer)
                if retrieved_chunks:
                    with st.expander("Sources"):
                        seen_sources = set()

                        for chunk in retrieved_chunks:
                            source = (
                                chunk["document_name"],
                                chunk["page_number"]
                            )

                            if source not in seen_sources:
                                st.write(
                                    f"📄 {chunk['document_name']} "
                                    f"— page {chunk['page_number']}"
                                )

                                seen_sources.add(source)
            except Exception as error:
                answer = (
                    "I could not contact the local model. Make sure Ollama is running "
                    f"and that `{model_name}` is installed.\n\nTechnical detail: `{error}`"
                )
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
