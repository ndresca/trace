from typing import Optional

from pydantic import BaseModel


class QuestionPayload(BaseModel):
    id: str
    text: str
    attribute_key: str


class GuessPayload(BaseModel):
    id: str
    name: str


class StartResponse(BaseModel):
    session_id: str
    question: QuestionPayload


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


class AnswerResponse(BaseModel):
    status: str
    next_question: Optional[QuestionPayload] = None
    guess: Optional[GuessPayload] = None
    remaining_candidates: int


class ContinueRequest(BaseModel):
    session_id: str


class GuessResponse(BaseModel):
    guess: GuessPayload
    score: float
    remaining_candidates: int
    questions_asked: int


class QuestionAnswer(BaseModel):
    question_id: str
    answer: str


class FeedbackRequest(BaseModel):
    session_id: str
    correct_entity_id: Optional[str] = None
    was_correct: bool
    questions_asked: list[QuestionAnswer]


class FeedbackResponse(BaseModel):
    status: str
