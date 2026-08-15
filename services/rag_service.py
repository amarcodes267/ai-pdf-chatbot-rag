from services.retrieval_service import RetrievalService
from services.llm_service import generate_answer
from utils.constants import TOP_K_RESULTS


class RAGService:
    """
    Handles the complete Retrieval-Augmented Generation (RAG) pipeline.
    """

    def __init__(self):
        self.retriever = RetrievalService()

    def answer_question(self, question: str) -> dict:
        """
        Generate an answer for the user's question.
        """

        results = self.retriever.retrieve(question, top_k=TOP_K_RESULTS)

        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        distances = results.get("distances", [])

        if not documents or not documents[0]:
            return {
                "answer": "I couldn't find any relevant information in the uploaded documents.",
                "sources": []
            }

        context = "\n\n".join(documents[0])

        answer = generate_answer(
            context=context,
            question=question
        )

        sources = []
        docs_list = documents[0]

        meta_list = metadatas[0] if metadatas and metadatas[0] else [None] * len(docs_list)
        dist_list = distances[0] if distances and distances[0] else [None] * len(docs_list)

        for idx, doc in enumerate(docs_list):
            meta = meta_list[idx] if idx < len(meta_list) else {}
            dist = dist_list[idx] if idx < len(dist_list) else None

            raw_distance = float(dist) if dist is not None else None
            similarity = round(1.0 / (1.0 + raw_distance), 4) if raw_distance is not None else None

            sources.append({
                "document": meta.get("source") if meta else None,
                "page": meta.get("page") if meta else None,
                "chunk": meta.get("chunk") if meta else idx,
                "similarity": similarity,
                "text": doc,
            })

        return {
            "answer": answer,
            "sources": sources,
        }
