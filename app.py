import streamlit as st
from components.sidebar import render_sidebar
from chat_ui import render_chat_ui


# --------------------------------------------------
# Page Configuration
# This must be the first Streamlit command
# --------------------------------------------------
st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)
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

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption("Built with ❤️ using Streamlit | AI PDF Chatbot (RAG)")    