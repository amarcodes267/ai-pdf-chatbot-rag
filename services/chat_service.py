import streamlit as st


class ChatService:
    """
    Handles chat history using Streamlit session state.
    """

    def __init__(self):
        """
        Initialize chat history.
        """
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    def add_user_message(self, message: str):
        """
        Add a user message to chat history.
        """
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": message
            }
        )

    def add_ai_message(self, message: str):
        """
        Add an AI response to chat history.
        """
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": message
            }
        )

    def get_chat_history(self):
        """
        Return the complete chat history.
        """
        return st.session_state.chat_history

    def clear_chat(self):
        """
        Clear the chat history.
        """
        st.session_state.chat_history = []