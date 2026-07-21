import faiss
import pickle
import json


def create_vector_store(embeddings):
    """
    Creates a FAISS vector index and stores the embeddings.
    """

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_vector_store(index, question_embedding, k=5):
    """
    Searches the FAISS index and returns distances and indices.
    """

    distances, indices = index.search(question_embedding, k)

    return distances, indices


def save_vector_store(index, file_path):
    """
    Saves the FAISS index to disk.
    """

    faiss.write_index(index, file_path)


def load_vector_store(file_path):
    """
    Loads the FAISS index from disk.
    """

    return faiss.read_index(file_path)


def save_chunks(chunks, file_path):
    """
    Saves text chunks using pickle.
    """

    with open(file_path, "wb") as file:
        pickle.dump(chunks, file)


def load_chunks(file_path):
    """
    Loads text chunks from disk.
    """

    with open(file_path, "rb") as file:
        return pickle.load(file)


def save_metadata(metadata, file_path):
    """
    Saves metadata as a JSON file.
    """

    with open(file_path, "w") as file:
        json.dump(metadata, file, indent=4)


def load_metadata(file_path):
    """
    Loads metadata from a JSON file.
    """

    with open(file_path, "r") as file:
        return json.load(file)