import os

from typing import Optional


def _openai_available() -> bool:
    try:
        import openai  # type: ignore

        return bool(os.environ.get("OPENAI_API_KEY"))
    except Exception:
        return False


def generate_answer(context: str, question: str, model: Optional[str] = None) -> str:
    if _openai_available():
        from openai import OpenAI

        api_key = os.environ.get("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)

        system_prompt = (
            "You are an assistant that answers questions using ONLY the provided "
            "context documents. If the answer is not present in the context, explicitly "
            "state that the information was not found in the provided documents. "
            "Be concise and do not invent facts."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ]

        try:
            resp = client.chat.completions.create(
                model=model or "gpt-4o-mini",
                messages=messages,
                temperature=0.0,
                max_tokens=512,
            )

            content = resp.choices[0].message.content
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
        + "\n\nNote: Set OPENAI_API_KEY to enable AI-generated answers."
    )

    return answer
