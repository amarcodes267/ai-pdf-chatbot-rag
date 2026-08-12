from services.retrieval_service import RetrievalService
from services.llm_service import generate_answer


class RAGService:
    """
    Handles the complete Retrieval-Augmented Generation (RAG) pipeline.
    """

    def __init__(self):
        self.retriever = RetrievalService()

    def answer_question(self, question: str) -> str:
        """
        Generate an answer for the user's question.
        """

        results = self.retriever.retrieve(question)

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

            sources.append({
                "document": meta.get("source") if meta else None,
                "page": meta.get("page") if meta else None,
                "chunk": meta.get("chunk") if meta else idx,
                "similarity": float(dist) if dist is not None else None,
                "text": doc,
            })

        return {
            "answer": answer,
            "sources": sources,
        }