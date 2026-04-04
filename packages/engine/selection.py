from typing import Optional

from .models import Question


def select_next_question(
    questions: list[Question],
    asked_question_ids: set[str],
) -> Optional[Question]:
    remaining_questions = [
        question
        for question in questions
        if question.enabled and question.id not in asked_question_ids
    ]

    if not remaining_questions:
        return None

    return max(remaining_questions, key=lambda question: question.priority)
