import streamlit as st
from components.sidebar import render_sidebar
from components.upload_box import render_upload_box


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


# --------------------------------------------------
# Main Page
# --------------------------------------------------
st.title("📄 AI PDF Chatbot")

st.markdown(
    """
Welcome to the **AI PDF Chatbot**.

This application allows you to:

- 📤 Upload PDF documents
- 📖 Extract and process document text
- 🔍 Search using semantic similarity
- 🤖 Ask questions about your document
- 📚 Receive answers based only on the uploaded PDF
"""
)

st.markdown("---")

# --------------------------------------------------
# Placeholder for PDF Upload
# (We'll implement this in the next step)
# --------------------------------------------------
st.header("📤 Upload Your PDF")
uploaded_file = render_upload_box()

st.info(
    "PDF upload functionality will be implemented in the next phase."
)

st.markdown("---")

# --------------------------------------------------
# Placeholder for Chat Section
# --------------------------------------------------
st.header("💬 Chat")

st.write(
    "Once a PDF has been uploaded and processed, "
    "you'll be able to ask questions here."
)

st.text_input(
    "Ask a question about your PDF:",
    placeholder="Example: What is the main topic of this document?",
    disabled=True,
)

st.button("Send", disabled=True)

st.markdown("---")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption("Built with ❤️ using Streamlit | AI PDF Chatbot (RAG)")    