import json
import sys
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from packages.engine.filtering import filter_entities
from packages.engine.models import Entity, Question
from packages.engine.scoring import score_entity
from packages.engine.selection import select_next_question
from services.api.models import (
    AnswerRequest,
    AnswerResponse,
    GuessPayload,
    QuestionPayload,
    StartSessionResponse,
)


QUESTIONS_PATH = ROOT / "data" / "questions" / "core_v1.json"
ENTITIES_PATH = ROOT / "data" / "seeds" / "entities_v1.jsonl"
ALLOWED_ANSWERS = {"yes", "probably_yes", "i_dont_know", "probably_no", "no"}


def load_questions() -> list[Question]:
    with QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        items = json.load(file)

    return [Question(**item) for item in items]


def load_entities() -> list[Entity]:
    with ENTITIES_PATH.open("r", encoding="utf-8") as file:
        return [Entity(**json.loads(line)) for line in file if line.strip()]


QUESTIONS = load_questions()
QUESTION_BY_ID = {question.id: question for question in QUESTIONS}
ENTITIES = load_entities()
SESSIONS: dict[str, dict] = {}

app = FastAPI(title="Trace API")


def to_question_payload(question: Question) -> QuestionPayload:
    return QuestionPayload(
        id=question.id,
        text=question.text,
        attribute_key=question.attribute_key,
    )


def rank_entities(answers: dict[str, str]) -> tuple[list[tuple[Entity, float]], int]:
    filtered = filter_entities(ENTITIES, answers)
    entities_to_rank = filtered or ENTITIES
    ranked = sorted(
        ((entity, score_entity(entity, answers)) for entity in entities_to_rank),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked, len(entities_to_rank)


def build_guess_response(entity: Entity, remaining_candidates: int) -> AnswerResponse:
    return AnswerResponse(
        status="guess",
        guess=GuessPayload(id=entity.id, name=entity.name),
        remaining_candidates=remaining_candidates,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/session/start", response_model=StartSessionResponse)
def start_session() -> StartSessionResponse:
    session_id = uuid.uuid4().hex
    first_question = select_next_question(
        QUESTIONS,
        asked_question_ids=set(),
        answered_attribute_keys=set(),
        ranked_entities=None,
        answers={},
    )
    if first_question is None:
        raise HTTPException(status_code=500, detail="No questions available")

    SESSIONS[session_id] = {
        "session_id": session_id,
        "asked_question_ids": set(),
        "answers": {},
        "ranked_entities": None,
        "question_count": 0,
        "current_question_id": first_question.id,
    }

    return StartSessionResponse(
        session_id=session_id,
        question=to_question_payload(first_question),
    )


@app.post("/session/{session_id}/answer", response_model=AnswerResponse)
def answer_question(session_id: str, body: AnswerRequest) -> AnswerResponse:
    session = SESSIONS.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if body.answer not in ALLOWED_ANSWERS:
        raise HTTPException(status_code=400, detail="Invalid answer")

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        raise HTTPException(status_code=400, detail="Session has no active question")

    current_question = QUESTION_BY_ID.get(current_question_id)
    if current_question is None:
        raise HTTPException(status_code=500, detail="Question not found")

    session["asked_question_ids"].add(current_question.id)
    session["answers"][current_question.attribute_key] = body.answer
    session["question_count"] += 1

    ranked_entities, remaining_candidates = rank_entities(session["answers"])
    session["ranked_entities"] = ranked_entities

    if remaining_candidates == 1:
        session["current_question_id"] = None
        return build_guess_response(ranked_entities[0][0], remaining_candidates)

    if len(ranked_entities) >= 2:
        top_score = ranked_entities[0][1]
        second_score = ranked_entities[1][1]
        if top_score - second_score >= 1.0:
            session["current_question_id"] = None
            return build_guess_response(ranked_entities[0][0], remaining_candidates)

    if session["question_count"] >= 5:
        session["current_question_id"] = None
        return build_guess_response(ranked_entities[0][0], remaining_candidates)

    next_question = select_next_question(
        QUESTIONS,
        asked_question_ids=session["asked_question_ids"],
        answered_attribute_keys=set(session["answers"].keys()),
        ranked_entities=ranked_entities,
        answers=session["answers"],
    )
    if next_question is None:
        session["current_question_id"] = None
        return build_guess_response(ranked_entities[0][0], remaining_candidates)

    session["current_question_id"] = next_question.id
    return AnswerResponse(
        status="question",
        next_question=to_question_payload(next_question),
        remaining_candidates=remaining_candidates,
    )
