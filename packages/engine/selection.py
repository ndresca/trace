from __future__ import annotations

import json
from pathlib import Path

from .models import Entity, Question


ROOT = Path(__file__).resolve().parents[2]
EXCLUSION_GROUPS_PATH = ROOT / "data" / "questions" / "exclusion_groups_v1.json"

with EXCLUSION_GROUPS_PATH.open("r", encoding="utf-8") as file:
    EXCLUSION_GROUPS: dict[str, list[str]] = json.load(file)


def select_next_question(
    questions: list[Question],
    asked_question_ids: set[str],
    answered_attribute_keys: set[str] | None = None,
    ranked_entities: list[tuple[Entity, float]] | None = None,
    answers: dict[str, str] | None = None,
) -> Question | None:
    excluded_attribute_keys: set[str] = set()

    if answers is not None:
        for attribute_key, answer in answers.items():
            if answer == "yes":
                excluded_attribute_keys.update(EXCLUSION_GROUPS.get(attribute_key, []))

    remaining_questions = [
        question
        for question in questions
        if question.enabled
        and question.id not in asked_question_ids
        and (
            answered_attribute_keys is None
            or question.attribute_key not in answered_attribute_keys
        )
        and question.attribute_key not in excluded_attribute_keys
    ]

    if not remaining_questions:
        return None

    if ranked_entities:
        top_entities = [entity for entity, _ in ranked_entities[:5]]

        def spread_score(question: Question) -> float:
            values = [
                entity.attributes.get(question.attribute_key, 0.5)
                for entity in top_entities
            ]
            return max(values) - min(values)

        return max(remaining_questions, key=spread_score)

    return max(remaining_questions, key=lambda question: question.priority)
