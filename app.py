import streamlit as st

from src.llm_client import ask_model, check_ollama_connection
from src.pdf_loader import extract_pdf_pages


st.set_page_config(
    page_title="UniMind AI",
    page_icon="📚",
    layout="wide",
)

st.title("📚 UniMind AI")
st.caption("A local AI study assistant for asking questions about university PDFs.")

with st.sidebar:
    st.header("Document")
    uploaded_file = st.file_uploader(
        "Upload one PDF",
        type=["pdf"],
        help="The starter version supports one text-based PDF at a time.",
    )

    st.header("Local model")
    model_name = st.text_input("Ollama model", value="gemma3:4b")

    if st.button("Check Ollama connection", use_container_width=True):
        ok, message = check_ollama_connection()
        if ok:
            st.success(message)
        else:
            st.error(message)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_pages" not in st.session_state:
    st.session_state.document_pages = []

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if uploaded_file is not None:
    if st.session_state.document_name != uploaded_file.name:
        try:
            pages = extract_pdf_pages(uploaded_file.getvalue())
            st.session_state.document_pages = pages
            st.session_state.document_name = uploaded_file.name
            st.session_state.messages = []
            st.success(
                f"Loaded {uploaded_file.name} with {len(pages)} pages containing text."
            )
        except ValueError as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"Could not read the PDF: {error}")

if st.session_state.document_name:
    st.info(
        f"Current document: **{st.session_state.document_name}** "
        f"({len(st.session_state.document_pages)} pages)"
    )
else:
    st.warning("Upload a PDF before asking a document question.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask a question about the uploaded PDF",
    disabled=not bool(st.session_state.document_pages),
)

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Reading the document and preparing an answer..."):
            try:
                answer = ask_model(
                    model=model_name,
                    question=question,
                    pages=st.session_state.document_pages,
                )
                st.markdown(answer)
            except Exception as error:
                answer = (
                    "I could not contact the local model. Make sure Ollama is running "
                    f"and that `{model_name}` is installed.\n\nTechnical detail: `{error}`"
                )
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
