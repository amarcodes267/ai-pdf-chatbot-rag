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

        # Retrieve relevant chunks
        results = self.retriever.retrieve(question)

        # Extract retrieved documents
        documents = results.get("documents", [])

        if not documents or not documents[0]:
            return "I couldn't find any relevant information in the uploaded document."

        # Combine retrieved chunks into a single context
        context = "\n\n".join(documents[0])

        # Generate answer using Ollama
        answer = generate_answer(
            context=context,
            question=question
        )

        return answer