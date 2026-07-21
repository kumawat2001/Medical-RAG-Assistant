import os
from pathlib import Path

from loader import load_pdfs
from chunker import create_chunks
from embeddings import create_embeddings

from vector_store import (
    create_vector_store,
    search_vector_store,
    save_vector_store,
    load_vector_store,
    save_chunks,
    load_chunks,
    save_metadata,
    load_metadata
)

# -------------------------------------------------
# Configuration
# -------------------------------------------------

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Project Paths

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data"

VECTORSTORE_FOLDER = PROJECT_ROOT / "vectorstore"

INDEX_PATH = VECTORSTORE_FOLDER / "index.faiss"
CHUNKS_PATH = VECTORSTORE_FOLDER / "chunks.pkl"
METADATA_PATH = VECTORSTORE_FOLDER / "metadata.json"


def build_vector_store():
    """
    Builds a new FAISS Vector Store from all PDFs
    inside the data folder.
    """

    documents = load_pdfs(DATA_FOLDER)

    pdf_files = sorted(
        document["pdf_name"]
        for document in documents
    )

    chunks = create_chunks(documents)

    embeddings = create_embeddings(chunks)

    index = create_vector_store(embeddings)

    metadata = {
        "pdf_files": pdf_files,
        "embedding_model": EMBEDDING_MODEL,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "num_chunks": len(chunks),
        "total_pdfs": len(pdf_files)
    }

    VECTORSTORE_FOLDER.mkdir(exist_ok=True)

    save_vector_store(index, str(INDEX_PATH))
    save_chunks(chunks, str(CHUNKS_PATH))
    save_metadata(metadata, str(METADATA_PATH))

    print("\nVector Store saved successfully!")

    return chunks, index


def initialize_retriever():
    """
    Loads an existing vector store if available.
    Otherwise creates a new one from all PDFs.
    """

    documents = load_pdfs(DATA_FOLDER)

    pdf_files = sorted(
        document["pdf_name"]
        for document in documents
    )

    current_metadata = {
        "pdf_files": pdf_files,
        "embedding_model": EMBEDDING_MODEL,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP
    }

    # -------------------------------------------------
    # Load Existing Vector Store
    # -------------------------------------------------

    if (
        INDEX_PATH.exists()
        and CHUNKS_PATH.exists()
        and METADATA_PATH.exists()
    ):

        saved_metadata = load_metadata(str(METADATA_PATH))

        if (
            saved_metadata["pdf_files"] == current_metadata["pdf_files"]
            and saved_metadata["embedding_model"] == current_metadata["embedding_model"]
            and saved_metadata["chunk_size"] == current_metadata["chunk_size"]
            and saved_metadata["chunk_overlap"] == current_metadata["chunk_overlap"]
        ):

            print("\nLoading existing FAISS Vector Store...")

            print(f"PDFs Loaded : {len(saved_metadata['pdf_files'])}")
            print(f"Embedding Model : {saved_metadata['embedding_model']}")
            print(f"Total Chunks : {saved_metadata['num_chunks']}")

            index = load_vector_store(str(INDEX_PATH))

            chunks = load_chunks(str(CHUNKS_PATH))

            return chunks, index

        print("\nMetadata changed.")
        print("Rebuilding Vector Store...\n")

        return build_vector_store()

    print("\nNo saved Vector Store found.")
    print("Creating a new Vector Store...\n")

    return build_vector_store()


def retrieve_context(question, chunks, index):
    """
    Retrieves the most relevant chunks along
    with their source information.
    """

    question_chunk = [
        {
            "text": question
        }
    ]

    question_embedding = create_embeddings(
        question_chunk
    )

    distances, indices = search_vector_store(
        index,
        question_embedding
    )

    retrieved_chunks = []

    for idx in indices[0]:
        retrieved_chunks.append(chunks[idx])

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    sources = []

    for chunk in retrieved_chunks:
        sources.append(
            {
                "pdf_name": chunk["pdf_name"],
                "page": chunk["page"]
            }
        )

    return context, sources