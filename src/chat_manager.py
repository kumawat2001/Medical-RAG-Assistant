import streamlit as st

WELCOME_MESSAGE = (
    "👋 Hello! I'm your Medical RAG Assistant.\n\n"
    "Upload your medical PDFs and ask me anything."
)


def initialize_chat():
    """Initialize chat history."""

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE,
            }
        ]


def get_chat_history():
    """Return all chat messages."""

    return st.session_state.messages


def add_user_message(message):
    """Store a user message."""

    st.session_state.messages.append(
        {
            "role": "user",
            "content": message,
        }
    )


def add_assistant_message(answer, sources):
    """Store an assistant response."""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )


def clear_chat():
    """Reset chat history."""

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE,
        }
    ]