from services.embedding_service import generate_embeddings
from services.vector_store import VectorStore


class RetrievalService:
    """
    Handles lightweight keyword retrieval from the local index.
    """

    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve the most relevant chunks for a query.
        """

        query = query.strip()
        if not query:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        # Generate embedding for the user query
        query_embedding = generate_embeddings([query])[0]

        # Search the local index.
        if self.vector_store.is_empty():
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results
