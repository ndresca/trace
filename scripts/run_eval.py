import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = ROOT / "data" / "questions" / "core_v1.json"
ENTITIES_PATH = ROOT / "data" / "seeds" / "entities_v1.jsonl"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from packages.engine.models import Entity, Question
from packages.engine.scoring import score_entity
from packages.engine.selection import select_next_question


def load_questions() -> list[Question]:
    with QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        items = json.load(file)

    return [Question(**item) for item in items]


def load_entities() -> list[Entity]:
    with ENTITIES_PATH.open("r", encoding="utf-8") as file:
        return [Entity(**json.loads(line)) for line in file if line.strip()]


def main() -> None:
    questions = load_questions()
    entities = load_entities()
    asked_question_ids = {"q001_real_person", "q002_alive"}
    answers = {
        "is_real_person": "yes",
        "is_alive": "yes",
        "is_female": "probably_yes",
        "is_musician": "yes",
        "is_actor": "probably_no",
        "is_politician": "no",
    }
    ranked_entities = sorted(
        ((entity, score_entity(entity, answers)) for entity in entities),
        key=lambda item: item[1],
        reverse=True,
    )
    next_question = select_next_question(questions, asked_question_ids)

    print(f"questions loaded: {len(questions)}")
    print(f"entities loaded: {len(entities)}")
    print(f"first question text: {questions[0].text}")
    print(f"first entity name: {entities[0].name}")
    print("top 5 entities:")

    for entity, score in ranked_entities[:5]:
        print(f"- {entity.name}: {score:.2f}")

    if next_question is not None:
        print(f"next question text: {next_question.text}")


if __name__ == "__main__":
    main()
