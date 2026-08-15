import os

from typing import Optional


def _gemini_available() -> bool:
    try:
        import google.genai  # type: ignore

        return bool(os.environ.get("GEMINI_API_KEY"))
    except Exception:
        return False


def generate_answer(context: str, question: str, model: Optional[str] = None) -> str:
    if _gemini_available():
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

        system_prompt = (
            "You are an assistant that answers questions using ONLY the provided "
            "context documents. If the answer is not present in the context, explicitly "
            "state that the information was not found in the provided documents. "
            "Be concise and do not invent facts."
        )

        try:
            response = client.models.generate_content(
                model=model or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
                contents=f"Context:\n{context}\n\nQuestion: {question}",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.0,
                    max_output_tokens=512,
                ),
            )

            content = response.text
            return content.strip() if content else "I could not generate an answer."
        except Exception as e:
            return f"LLM error: {e}"

    # Fallback: simple heuristic answer when no external LLM is configured
    snippet = context[:1500]
    answer = (
        "No LLM is configured. Here is the most relevant context from your documents:\n\n"
        + snippet
        + "\n\nQuestion: "
        + question
        + "\n\nNote: Set GEMINI_API_KEY to enable AI-generated answers."
    )

    return answer
