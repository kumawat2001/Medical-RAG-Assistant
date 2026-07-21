import streamlit as st

from retriever import (
    initialize_retriever,
    retrieve_context,
    build_vector_store
)

from llm import generate_answer
from pdf_uploader import save_uploaded_pdf

from chat_manager import (
    initialize_chat,
    get_chat_history,
    add_user_message,
    add_assistant_message,
    clear_chat,
)

from memory import (
    initialize_memory,
    update_memory,
    get_contextual_query,
    clear_memory,
)

from database import create_users_table
from auth import register_user, login_user


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Medical RAG Assistant",
    page_icon="🩺",
    layout="wide"
)

create_users_table()

# -------------------------------------------------
# Load Retriever
# -------------------------------------------------

# -------------------------------------------------
# Load Retriever
# -------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_retriever():
    return initialize_retriever()


with st.spinner("Loading Medical Knowledge Base..."):
    chunks, index = load_retriever()

# No knowledge base loaded yet
if index is None:
    st.info("📄 No medical PDF uploaded yet. Please upload a PDF from the sidebar to build the knowledge base.")

# -------------------------------------------------
# Initialize Chat
# -------------------------------------------------

initialize_chat()
initialize_memory()

# -------------------------------------------------
# Authentication
# -------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.logged_in:

    st.title("🩺 Medical RAG Assistant")
    st.subheader("Login to Continue")

    login_tab, signup_tab = st.tabs(["🔑 Login", "📝 Sign Up"])

    # ---------------- LOGIN ---------------- #

    with login_tab:

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            success, result = login_user(
                username,
                password
            )

            if success:

                st.session_state.logged_in = True
                st.session_state.user = result

                st.success("✅ Login successful!")
                st.rerun()

            else:

                st.error(result)

    # ---------------- SIGN UP ---------------- #

    with signup_tab:

        new_username = st.text_input(
            "Choose Username",
            key="signup_username"
        )

        new_password = st.text_input(
            "Choose Password",
            type="password",
            key="signup_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            success, message = register_user(
                new_username,
                new_password
            )

            if success:

                st.success(message)

            else:

                st.error(message)

    st.stop()





# -------------------------------------------------
# Sidebar
# -------------------------------------------------

with st.sidebar:

    st.success(
        f"👋 Welcome, {st.session_state.user['username']}"
    )

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.divider()

    st.header("📚 Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload a medical PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success(f"Selected File:\n{uploaded_file.name}")

        if st.button("📤 Upload PDF", use_container_width=True):

            with st.spinner("Updating Knowledge Base..."):

                # Save uploaded PDF
                save_uploaded_pdf(uploaded_file)

                # Rebuild vector store
                build_vector_store()

                # Clear Streamlit cache
                st.cache_resource.clear()

                # Reload retriever
                chunks, index = load_retriever()

            st.success("✅ Knowledge Base Updated!")
            st.info("You can now ask questions from the uploaded PDF.")

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):

        clear_chat()
        clear_memory()

        st.rerun()

    st.divider()

    st.header("ℹ About")

    st.write(
        """
        **Medical RAG Assistant**

        Upload medical PDFs and ask
        questions using Retrieval
        Augmented Generation (RAG).

        **Tech Stack**
        - LangChain
        - FAISS
        - Hugging Face
        - Streamlit
        """
    )


# -------------------------------------------------
# Main Page
# -------------------------------------------------

st.title("🩺 Medical RAG Assistant")

st.caption("Ask questions from your medical documents.")


# -------------------------------------------------
# Display Chat History
# -------------------------------------------------

messages = get_chat_history()

for message in messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and "sources" in message:

            st.markdown("**📄 Sources**")

            for source in message["sources"]:

                st.write(
                    f"✅ {source['pdf_name']} (Page {source['page']})"
                )


# -------------------------------------------------
# Chat Input
# -------------------------------------------------

prompt = st.chat_input(
    "Ask a medical question..."
)

# -------------------------------------------------
# Generate Response
# -------------------------------------------------

if prompt:

    if index is None:
        st.warning("📄 Please upload a medical PDF first.")
        st.stop()

    # Store and display user message
    add_user_message(prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve context and generate answer
    with st.spinner("Searching medical knowledge..."):

        # Build a contextual query using previous conversation
        contextual_query = get_contextual_query(prompt)

        context, sources = retrieve_context(
            contextual_query,
            chunks,
            index
        )

        answer = generate_answer(
            context,
            prompt
        )

    # Remove duplicate sources
    unique_sources = []
    seen = set()

    for source in sources:

        key = (
            source["pdf_name"],
            source["page"]
        )

        if key not in seen:

            seen.add(key)

            unique_sources.append(
                {
                    "pdf_name": source["pdf_name"],
                    "page": source["page"]
                }
            )

    # Display assistant response
    with st.chat_message("assistant"):

        st.markdown(answer)

        if unique_sources:

            st.markdown("**📄 Sources**")

            for source in unique_sources:

                st.write(
                    f"✅ {source['pdf_name']} "
                    f"(Page {source['page']})"
                )

    # Save assistant response
    add_assistant_message(
        answer,
        unique_sources
    )

    # Save conversation to memory
    update_memory(
        prompt,
        answer
    )

    # Refresh UI to show the updated conversation
    st.rerun()
