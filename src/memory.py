import streamlit as st

MAX_HISTORY = 3


def initialize_memory():
    """
    Initialize conversation memory.
    """

    if "conversation_memory" not in st.session_state:
        st.session_state.conversation_memory = []


def update_memory(user_message, assistant_message):
    """
    Store the latest user-assistant interaction.
    """

    st.session_state.conversation_memory.append(
        {
            "user": user_message,
            "assistant": assistant_message
        }
    )

    # Keep only the most recent conversations
    if len(st.session_state.conversation_memory) > MAX_HISTORY:
        st.session_state.conversation_memory.pop(0)


def get_contextual_query(current_question):
    """
    Build a contextual query using recent conversation.
    """

    if not st.session_state.conversation_memory:
        return current_question

    conversation = ""

    for chat in st.session_state.conversation_memory:

        conversation += (
            f"User: {chat['user']}\n"
            f"Assistant: {chat['assistant']}\n\n"
        )

    contextual_query = (
        f"Previous Conversation:\n"
        f"{conversation}"
        f"Current Question:\n"
        f"{current_question}"
    )

    return contextual_query


def clear_memory():
    """
    Clear conversation memory.
    """

    st.session_state.conversation_memory = []