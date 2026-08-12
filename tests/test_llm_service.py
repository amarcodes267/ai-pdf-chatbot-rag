from services.llm_service import generate_answer


def test_generate_answer_returns_string():
    context = "This document describes the lifecycle of an apple."
    question = "What is described?"

    resp = generate_answer(context=context, question=question)

    assert isinstance(resp, str)
    assert len(resp) > 0
