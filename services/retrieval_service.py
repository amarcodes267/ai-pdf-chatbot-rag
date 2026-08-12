from services.embedding_service import generate_embeddings
from services.vector_store import VectorStore


class RetrievalService:
    """
    Handles semantic retrieval from ChromaDB.
    """

    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve the most relevant chunks for a query.
        """

        # Generate embedding for the user query
        query_embedding = generate_embeddings([query])[0]

        # Search ChromaDB
        if self.vector_store.is_empty():
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results