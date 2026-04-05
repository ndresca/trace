import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = ROOT / "data" / "questions" / "core_v1.json"
ENTITIES_PATH = ROOT / "data" / "seeds" / "entities_v1.jsonl"
ALLOWED_ANSWERS = {
    "yes",
    "probably_yes",
    "i_dont_know",
    "probably_no",
    "no",
}

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


def rank_entities(entities: list[Entity], answers: dict[str, str]) -> list[tuple[Entity, float]]:
    return sorted(
        ((entity, score_entity(entity, answers)) for entity in entities),
        key=lambda item: item[1],
        reverse=True,
    )


def prompt_for_answer(question: Question) -> str:
    while True:
        answer = input(f"{question.text}\n> ").strip()
        if answer in ALLOWED_ANSWERS:
            return answer

        print("Please answer with: yes, probably_yes, i_dont_know, probably_no, or no.")


def main() -> None:
    questions = load_questions()
    entities = load_entities()
    asked_question_ids: set[str] = set()
    answers: dict[str, str] = {}
    ranked_entities: list[tuple[Entity, float]] | None = None
    question_count = 0

    print("Think of a famous person.")

    while question_count < 5:
        next_question = select_next_question(
            questions,
            asked_question_ids,
            answered_attribute_keys=set(answers.keys()),
            ranked_entities=ranked_entities,
            answers=answers,
        )
        if next_question is None:
            break

        answer = prompt_for_answer(next_question)
        asked_question_ids.add(next_question.id)
        answers[next_question.attribute_key] = answer
        question_count += 1

        filtered_entities = filter_entities(entities, answers)
        entities_to_rank = filtered_entities or entities
        ranked_entities = rank_entities(entities_to_rank, answers)
        print(f"remaining candidates: {len(entities_to_rank)}")

        if len(entities_to_rank) == 1:
            print("Final top candidates:")
            for entity, score in ranked_entities[:3]:
                print(f"- {entity.name}: {score:.2f}")
            print(f"I think it is: {entities_to_rank[0].name}")
            return

        print("Top 3 candidates:")
        for entity, score in ranked_entities[:3]:
            print(f"- {entity.name}: {score:.2f}")

        if len(ranked_entities) >= 2:
            top_entity, top_score = ranked_entities[0]
            _, second_score = ranked_entities[1]
            score_gap = top_score - second_score
            print(f"score gap: {score_gap:.2f}")

            if score_gap >= 1.0:
                print(f"I think it is: {top_entity.name}")
                return

    print("Game over.")


if __name__ == "__main__":
    main()
