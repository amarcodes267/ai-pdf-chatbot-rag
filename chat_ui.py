import streamlit as st
from pathlib import Path

from components.upload_box import render_upload_box
from components.sidebar import render_sidebar
from services.pdf_service import save_pdf
from services.text_extractor import extract_text
from services.text_cleaner import clean_text
from services.chunk_service import create_chunks_from_pages
from services.embedding_service import generate_embeddings
from services.vector_store import VectorStore
from services.chat_service import ChatService
from services.rag_service import RAGService
from utils.constants import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS


def _already_indexed(vector_store: VectorStore, filename: str) -> bool:
    try:
        results = vector_store.collection.get(
            where={"source": filename},
            limit=1,
        )
        return bool(results.get("ids"))
    except Exception:
        return False


def render_chat_ui():
    chat = ChatService()
    rag = RAGService()
    vector_store = VectorStore()

    st.header("📤 Upload and Process PDFs")

    uploaded_files = render_upload_box()

    if uploaded_files:
        if not isinstance(uploaded_files, list):
            uploaded_files = [uploaded_files]

        if st.button("Process uploaded PDF(s)"):
            with st.spinner("Processing PDFs — extracting, chunking, and creating embeddings..."):
                for uploaded in uploaded_files:
                    try:
                        if _already_indexed(vector_store, uploaded.name):
                            st.info(f"'{uploaded.name}' is already indexed. Skipping.")
                            continue

                        saved_path = save_pdf(uploaded)
                        page_texts = extract_text(Path(saved_path))

                        cleaned_pages = [clean_text(p) for p in page_texts]

                        chunks, metadatas = create_chunks_from_pages(
                            cleaned_pages,
                            filename=uploaded.name,
                            chunk_size=CHUNK_SIZE,
                            chunk_overlap=CHUNK_OVERLAP,
                        )

                        if not chunks:
                            st.warning(f"No text extracted from {uploaded.name}.")
                            continue

                        embeddings = generate_embeddings(chunks)

                        if not embeddings:
                            st.error("Embedding generation failed.")
                            continue

                        vector_store.add_documents(chunks, embeddings, metadatas=metadatas)

                        st.success(f"Processed and indexed: {uploaded.name}")

                    except Exception as e:
                        st.error(f"Error processing {uploaded.name}: {e}")

    st.markdown("---")

    st.header("💬 Chat")

    cols = st.columns([3, 1])

    with cols[0]:
        question = st.text_input("Ask a question about your documents:", key="question_input")

    with cols[1]:
        send = st.button("Send")
        clear = st.button("Clear Chat")

    if clear:
        chat.clear_chat()
        st.rerun()

    sources = []

    if send:
        if not question or question.strip() == "":
            st.warning("Please enter a question.")
        else:
            if vector_store.is_empty():
                st.info("No documents indexed yet. Upload and process PDFs first.")
            else:
                with st.spinner("Searching for relevant context and generating an answer..."):
                    chat.add_user_message(question)

                    try:
                        response = rag.answer_question(question)

                        if isinstance(response, dict):
                            answer = response.get("answer", "")
                            sources = response.get("sources", [])
                        else:
                            answer = str(response)
                            sources = []

                        chat.add_ai_message(answer)

                    except Exception as e:
                        st.error(f"Error generating answer: {e}")

    st.markdown("---")

    st.subheader("Conversation")
    history = chat.get_chat_history()

    if not history:
        st.info("No messages yet. Start by asking a question.")
    else:
        for msg in history:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                st.markdown(f"**You:** {content}")
            else:
                st.markdown(f"**Assistant:** {content}")

    if sources:
        st.markdown("---")
        st.subheader("Sources")
        for src in sources:
            doc = src.get("document") or "Unknown"
            page = src.get("page") or "-"
            chunk = src.get("chunk") or "-"
            sim = src.get("similarity")
            text = src.get("text") or ""

            with st.container():
                header_cols = st.columns([1, 4])
                with header_cols[0]:
                    st.markdown(f"**{doc}**")
                with header_cols[1]:
                    if sim is not None:
                        st.markdown(f"Page: {page} • Chunk: {chunk} • Similarity: {sim:.3f}")
                    else:
                        st.markdown(f"Page: {page} • Chunk: {chunk}")

                st.write(text[:800] + ("..." if len(text) > 800 else ""))


def render_main():
    render_sidebar()
    st.markdown("---")

    st.title("📄 AI PDF Chatbot")

    st.markdown(
        """
        Welcome to the **AI PDF Chatbot**.

        Upload PDF documents, process them, and ask questions using retrieval-augmented generation.
        """
    )

    st.markdown("---")

    render_chat_ui()

    st.markdown("---")

    st.caption("Built with ❤️ using Streamlit | AI PDF Chatbot (RAG)")
