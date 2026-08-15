import streamlit as st
from chat_ui import render_main


st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# ENTRY POINT
# ==================================================
# Add your custom Streamlit logic here before/after
# the main render, e.g. authentication, branding,
# experimental features, or route switching.
# ==================================================

render_main()
