import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = ROOT / "data" / "questions" / "core_v1.json"
ENTITIES_PATH = ROOT / "data" / "seeds" / "entities_v1.jsonl"
GOLD_CASES_PATH = ROOT / "data" / "eval" / "gold_cases_v1.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from packages.engine.models import Entity, Question
from packages.engine.filtering import filter_entities
from packages.engine.scoring import score_entity
from packages.engine.selection import select_next_question


def load_questions() -> list[Question]:
    with QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        items = json.load(file)

    return [Question(**item) for item in items]


def load_entities() -> list[Entity]:
    with ENTITIES_PATH.open("r", encoding="utf-8") as file:
        return [Entity(**json.loads(line)) for line in file if line.strip()]


def load_gold_cases() -> list[dict]:
    with GOLD_CASES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    questions = load_questions()
    entities = load_entities()
    gold_cases = load_gold_cases()

    print(f"questions loaded: {len(questions)}")
    print(f"entities loaded: {len(entities)}")
    print(f"first question text: {questions[0].text}")
    print(f"first entity name: {entities[0].name}")

    total_rank = 0
    top1_hits = 0
    total_questions_asked = 0
    failures: list[tuple[str, str, list[str]]] = []

    for case in gold_cases:
        target_entity_id = case["target_entity_id"]
        case_answers = case["answers"]
        asked_question_ids: set[str] = set()
        asked_attribute_keys: list[str] = []
        answers_so_far: dict[str, str] = {}
        ranked_entities: list[tuple[Entity, float]] | None = None
        questions_asked = 0

        while questions_asked < 5:
            next_question = select_next_question(
                questions,
                asked_question_ids,
                answered_attribute_keys=set(answers_so_far.keys()),
                ranked_entities=ranked_entities,
                answers=answers_so_far,
            )
            if (
                next_question is not None
                and next_question.attribute_key not in case_answers
            ):
                fallback_question = next(
                    (
                        question
                        for question in questions
                        if question.enabled
                        and question.id not in asked_question_ids
                        and question.attribute_key not in answers_so_far
                        and question.attribute_key in case_answers
                    ),
                    None,
                )
                if fallback_question is not None:
                    next_question = fallback_question
            if next_question is None:
                break

            answer = case_answers.get(next_question.attribute_key, "i_dont_know")
            asked_question_ids.add(next_question.id)
            asked_attribute_keys.append(next_question.attribute_key)
            answers_so_far[next_question.attribute_key] = answer
            questions_asked += 1

            filtered_entities = filter_entities(entities, answers_so_far)
            entities_to_rank = filtered_entities or entities
            ranked_entities = sorted(
                ((entity, score_entity(entity, answers_so_far)) for entity in entities_to_rank),
                key=lambda item: item[1],
                reverse=True,
            )

            if len(entities_to_rank) == 1:
                break

            if len(ranked_entities) >= 2:
                top_score = ranked_entities[0][1]
                second_score = ranked_entities[1][1]
                score_gap = top_score - second_score
                if score_gap >= 1.0:
                    break

        if ranked_entities is None:
            ranked_entities = sorted(
                ((entity, score_entity(entity, answers_so_far)) for entity in entities),
                key=lambda item: item[1],
                reverse=True,
            )

        ranked_entity_ids = [entity.id for entity, _ in ranked_entities]
        rank = ranked_entity_ids.index(target_entity_id) + 1
        top_entity_id = ranked_entity_ids[0]

        total_rank += rank
        total_questions_asked += questions_asked
        if rank == 1:
            top1_hits += 1
        else:
            failures.append((target_entity_id, top_entity_id, asked_attribute_keys))

        print(
            f"{target_entity_id}: questions={questions_asked} rank={rank} "
            f"top_guess={top_entity_id}"
        )
        print(f"  asked={','.join(asked_attribute_keys)}")

    total_cases = len(gold_cases)
    top1_accuracy = top1_hits / total_cases if total_cases else 0.0
    average_rank = total_rank / total_cases if total_cases else 0.0
    average_questions_asked = total_questions_asked / total_cases if total_cases else 0.0

    print("failure summary:")
    for target_entity_id, top_entity_id, asked_attribute_keys in failures:
        print(
            f"FAIL {target_entity_id}: top_guess={top_entity_id} "
            f"asked={','.join(asked_attribute_keys)}"
        )

    print(f"total cases: {total_cases}")
    print(f"top1 accuracy: {top1_accuracy:.2f}")
    print(f"average rank: {average_rank:.2f}")
    print(f"average questions asked: {average_questions_asked:.2f}")


if __name__ == "__main__":
    main()
