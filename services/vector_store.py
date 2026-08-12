from pathlib import Path

import chromadb


CHROMA_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "pdf_documents"


class VectorStore:
    """
    Handles all ChromaDB operations.
    """

    def __init__(self):
        """
        Initialize ChromaDB.
        """

        # Create the database directory
        Path(CHROMA_DB_PATH).mkdir(
            parents=True,
            exist_ok=True
        )

        # Initialize persistent client
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

        # Create or load collection
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    def add_documents(self, chunks, embeddings, metadatas=None):
        """
        Store chunks and embeddings.
        """
        from uuid import uuid4

        ids = [str(uuid4()) for _ in range(len(chunks))]
        if metadatas is None:
            metadatas = [
                {
                    "source": None,
                    "page": None,
                    "chunk": idx,
                }
                for idx in range(len(chunks))
            ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(self, query_embedding, top_k=5):
        """
        Search similar chunks.
        """

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results

    def is_empty(self) -> bool:
        """
        Return True if the collection appears empty. Uses collection.count() when available.
        """
        try:
            count = getattr(self.collection, "count", None)
            if callable(count):
                return count() == 0

            # Fallback: attempt a small query and see if documents returned
            res = self.collection.query(query_embeddings=[[0.0]*1], n_results=1)
            docs = res.get("documents", [])
            return not docs or not docs[0]
        except Exception:
            return False

    def clear_database(self):
        """
        Delete all stored vectors.
        """

        self.client.delete_collection(
            COLLECTION_NAME
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )