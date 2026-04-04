import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = ROOT / "data" / "questions" / "core_v1.json"
ENTITIES_PATH = ROOT / "data" / "seeds" / "entities_v1.jsonl"


def load_questions() -> list[dict]:
    with QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_entities() -> list[dict]:
    with ENTITIES_PATH.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def main() -> None:
    questions = load_questions()
    entities = load_entities()

    print(f"questions loaded: {len(questions)}")
    print(f"entities loaded: {len(entities)}")
    print(f"first question text: {questions[0]['text']}")
    print(f"first entity name: {entities[0]['name']}")


if __name__ == "__main__":
    main()
