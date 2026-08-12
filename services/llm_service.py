import os
import json

from typing import Optional


def _openai_available() -> bool:
    try:
        import openai  # type: ignore

        return bool(os.environ.get("OPENAI_API_KEY"))
    except Exception:
        return False


def generate_answer(context: str, question: str, model: Optional[str] = None) -> str:
    if _openai_available():
        import openai  # type: ignore

        api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_key = api_key

        system_prompt = (
            "You are an assistant that answers user questions using only the provided context. "
            "If the answer is not in the context, say you don't know. Be concise."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ]

        try:
            resp = openai.ChatCompletion.create(
                model=model or "gpt-3.5-turbo",
                messages=messages,
                temperature=0.0,
                max_tokens=512,
            )

            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"LLM error: {e}"

    # Fallback: simple heuristic answer when no external LLM is configured
    snippet = context[:1500]
    answer = (
        "Using local fallback (no LLM configured). Here is relevant context summary:\n\n"
        + snippet
        + "\n\nQuestion: "
        + question
        + "\n\nNote: Configure OPENAI_API_KEY to enable better responses."
    )

    return answer
