"""
Embedding generation service.

The SentenceTransformer model is loaded LAZILY — only when embeddings
are actually generated — so that the app starts up fast and uses less
memory. This is important on constrained hosts such as Render's free
tier, where loading torch + the model at import time would exceed the
available RAM and crash the server before the UI even loads.
"""

from functools import lru_cache


@lru_cache(maxsize=1)
def _get_embedding_model():
    """
    Import and load the embedding model once, on first use.

    Returns:
        SentenceTransformer: The loaded embedding model instance.
    """
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


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

    model = _get_embedding_model()

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embeddings.tolist()