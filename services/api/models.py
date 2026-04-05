from typing import Optional

from pydantic import BaseModel


class QuestionPayload(BaseModel):
    id: str
    text: str
    attribute_key: str


class GuessPayload(BaseModel):
    id: str
    name: str


class StartSessionResponse(BaseModel):
    session_id: str
    question: QuestionPayload


class AnswerRequest(BaseModel):
    answer: str


class AnswerResponse(BaseModel):
    status: str
    next_question: Optional[QuestionPayload] = None
    guess: Optional[GuessPayload] = None
    remaining_candidates: int
