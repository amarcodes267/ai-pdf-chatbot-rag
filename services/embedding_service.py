from sentence_transformers import SentenceTransformer

# Load the embedding model only once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text chunks.

    Args:
        chunks (list[str]): List of cleaned text chunks.

    Returns:
        list[list[float]]: List of embedding vectors.
    """

    if not chunks:
        return []

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embeddings.tolist()