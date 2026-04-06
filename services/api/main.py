import json
import sys
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from packages.engine.models import Entity, Question
from packages.engine.game import next_action, rank_entities
from services.api.models import (
    AnswerRequest,
    AnswerResponse,
    ContinueRequest,
    GuessPayload,
    GuessResponse,
    QuestionPayload,
    StartResponse,
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
QUESTION_BY_ID = {q.id: q for q in QUESTIONS}
ENTITIES = load_entities()
SESSIONS: dict[str, dict] = {}

app = FastAPI(title="Trace API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_session(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


def _eligible_entities(session: dict) -> list:
    excluded = session.get("excluded_entity_ids", set())
    if not excluded:
        return ENTITIES
    return [e for e in ENTITIES if e.id not in excluded]


def _question_payload(q: Question) -> QuestionPayload:
    return QuestionPayload(id=q.id, text=q.text, attribute_key=q.attribute_key)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/start", response_model=StartResponse)
def start() -> StartResponse:
    session_id = uuid.uuid4().hex

    result = next_action(
        QUESTIONS, ENTITIES,
        asked_question_ids=set(),
        answers={},
        question_count=0,
    )

    if result["action"] != "ask":
        raise HTTPException(status_code=500, detail="No questions available")

    SESSIONS[session_id] = {
        "asked_question_ids": set(),
        "answers": {},
        "question_count": 0,
        "current_question_id": result["question"].id,
        "excluded_entity_ids": set(),
    }

    return StartResponse(
        session_id=session_id,
        question=_question_payload(result["question"]),
    )


@app.post("/answer", response_model=AnswerResponse)
def answer(body: AnswerRequest) -> AnswerResponse:
    session = _get_session(body.session_id)

    if body.answer not in ALLOWED_ANSWERS:
        raise HTTPException(status_code=400, detail="Invalid answer")

    current_qid = session.get("current_question_id")
    if not current_qid:
        raise HTTPException(status_code=400, detail="No active question — call GET /guess")

    question = QUESTION_BY_ID.get(current_qid)
    if question is None:
        raise HTTPException(status_code=500, detail="Question not found")

    session["asked_question_ids"].add(question.id)
    session["answers"][question.attribute_key] = body.answer
    session["question_count"] += 1

    result = next_action(
        QUESTIONS, _eligible_entities(session),
        asked_question_ids=session["asked_question_ids"],
        answers=session["answers"],
        question_count=session["question_count"],
    )

    if result["action"] == "guess":
        session["current_question_id"] = None
        return AnswerResponse(
            status="guess",
            guess=GuessPayload(id=result["entity"].id, name=result["entity"].name),
            remaining_candidates=result["remaining_candidates"],
        )

    session["current_question_id"] = result["question"].id
    return AnswerResponse(
        status="question",
        next_question=_question_payload(result["question"]),
        remaining_candidates=result["remaining_candidates"],
    )


@app.post("/continue", response_model=AnswerResponse)
def continue_game(body: ContinueRequest) -> AnswerResponse:
    session = _get_session(body.session_id)

    ranked = rank_entities(_eligible_entities(session), session["answers"])
    if not ranked:
        raise HTTPException(status_code=400, detail="No candidates remaining")

    top_entity = ranked[0][0]
    session["excluded_entity_ids"].add(top_entity.id)

    eligible = _eligible_entities(session)
    result = next_action(
        QUESTIONS, eligible,
        asked_question_ids=session["asked_question_ids"],
        answers=session["answers"],
        question_count=session["question_count"],
    )

    if result["action"] == "guess":
        session["current_question_id"] = None
        return AnswerResponse(
            status="guess",
            guess=GuessPayload(id=result["entity"].id, name=result["entity"].name),
            remaining_candidates=result["remaining_candidates"],
        )

    session["current_question_id"] = result["question"].id
    return AnswerResponse(
        status="question",
        next_question=_question_payload(result["question"]),
        remaining_candidates=result["remaining_candidates"],
    )


@app.get("/guess", response_model=GuessResponse)
def guess(session_id: str) -> GuessResponse:
    session = _get_session(session_id)

    ranked = rank_entities(ENTITIES, session["answers"])
    if not ranked:
        raise HTTPException(status_code=500, detail="No entities to rank")

    top_entity, top_score = ranked[0]
    return GuessResponse(
        guess=GuessPayload(id=top_entity.id, name=top_entity.name),
        score=top_score,
        remaining_candidates=len(ranked),
        questions_asked=session["question_count"],
    )
