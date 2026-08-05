import streamlit as st


def render_sidebar():
    """
    Displays the application's sidebar.
    """

    with st.sidebar:

        st.title("📚 AI PDF Chatbot")

        st.markdown("---")

        st.subheader("Project")

        st.write("Retrieval-Augmented Generation (RAG)")

        st.markdown("---")

        st.subheader("Tech Stack")

        st.markdown("""
- Streamlit
- LangChain
- ChromaDB
- Sentence Transformers
- Ollama
- PyMuPDF
""")

        st.markdown("---")

        st.info("Upload a PDF to start chatting.")