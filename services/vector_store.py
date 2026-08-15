"""A compact JSON-backed vector store for single-instance deployments."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STORE_PATH = PROJECT_ROOT / "data" / "document_index.json"


class VectorStore:
    """Persist and search normalized vectors without ChromaDB."""

    def __init__(self):
        self._documents = self._load_documents()

    @staticmethod
    def _load_documents() -> list[dict]:
        if not STORE_PATH.exists():
            return []
        try:
            data = json.loads(STORE_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def _save_documents(self) -> None:
        STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = STORE_PATH.with_suffix(".tmp")
        temporary_path.write_text(json.dumps(self._documents), encoding="utf-8")
        temporary_path.replace(STORE_PATH)

    def has_source(self, filename: str) -> bool:
        return any(item["metadata"].get("source") == filename for item in self._documents)

    def add_documents(self, chunks, embeddings, metadatas=None):
        if len(chunks) != len(embeddings):
            raise ValueError("Each document chunk must have exactly one embedding.")
        if metadatas is not None and len(chunks) != len(metadatas):
            raise ValueError("Each document chunk must have exactly one metadata entry.")

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            metadata = metadatas[index] if metadatas else {
                "source": "Unknown", "page": 0, "chunk": index + 1
            }
            self._documents.append({
                "id": str(uuid4()), "document": chunk, "embedding": embedding,
                "metadata": metadata,
            })
        self._save_documents()

    def search(self, query_embedding, top_k=5):
        if not self._documents:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        def similarity(item: dict) -> float:
            return sum(a * b for a, b in zip(query_embedding, item["embedding"]))

        ranked = sorted(self._documents, key=similarity, reverse=True)[:top_k]
        return {
            "documents": [[item["document"] for item in ranked]],
            "metadatas": [[item["metadata"] for item in ranked]],
            "distances": [[1.0 - similarity(item) for item in ranked]],
        }

    def is_empty(self) -> bool:
        return not self._documents

    def clear_database(self):
        self._documents = []
        if STORE_PATH.exists():
            STORE_PATH.unlink()
