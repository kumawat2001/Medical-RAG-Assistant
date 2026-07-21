from sentence_transformers import SentenceTransformer

# Load the embedding model only once
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def create_embeddings(chunks):
    """
    Converts chunk text into embedding vectors.
    """

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(texts)

    return embeddings