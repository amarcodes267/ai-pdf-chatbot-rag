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

    def add_documents(self, chunks, embeddings):
        """
        Store chunks and embeddings.
        """

        ids = [
            f"chunk_{i}"
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings
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