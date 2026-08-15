"""Small, dependency-free embeddings suitable for low-memory deployments.

The vectors use a stable hash of normalized words. They provide lightweight
keyword relevance without downloading a transformer model or loading PyTorch.
"""

from hashlib import blake2b
import re


EMBEDDING_DIMENSIONS = 256
TOKEN_PATTERN = re.compile(r"\b\w+\b", re.UNICODE)


def _token_index(token: str) -> int:
    digest = blake2b(token.encode("utf-8"), digest_size=4).digest()
    return int.from_bytes(digest, "big") % EMBEDDING_DIMENSIONS


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """Create normalized hashed bag-of-words vectors for text chunks."""
    embeddings: list[list[float]] = []
    for chunk in chunks:
        vector = [0.0] * EMBEDDING_DIMENSIONS
        for token in TOKEN_PATTERN.findall(chunk.lower()):
            vector[_token_index(token)] += 1.0
        magnitude = sum(value * value for value in vector) ** 0.5
        if magnitude:
            vector = [value / magnitude for value in vector]
        embeddings.append(vector)
    return embeddings
