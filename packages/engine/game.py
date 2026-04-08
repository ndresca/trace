"""Game loop decisions: when to ask, when to guess.

Stateless. Takes current game state, returns the next action.
"""

from __future__ import annotations

from .filtering import filter_entities
from .models import Entity, Question
from .scoring import score_entity
from .selection import select_next_question

SCORE_GAP_THRESHOLD = 1.0
STALL_WINDOW = 5
STALL_MIN_IMPROVEMENT = 0.05


def rank_entities(
    entities: list[Entity], answers: dict[str, str]
) -> list[tuple[Entity, float]]:
    filtered = filter_entities(entities, answers)
    pool = filtered or entities
    ranked = sorted(
        ((e, score_entity(e, answers)) for e in pool),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked


def _current_gap(ranked_entities: list[tuple[Entity, float]]) -> float:
    if len(ranked_entities) < 2:
        return 0.0
    return ranked_entities[0][1] - ranked_entities[1][1]


def _is_stalled(
    gap_history: list[float],
    pool_history: list[int] | None = None,
) -> bool:
    """True if the score gap hasn't improved AND the pool hasn't shrunk over the last 5 entries."""
    if len(gap_history) < STALL_WINDOW:
        return False
    recent_gaps = gap_history[-STALL_WINDOW:]
    best_improvement = max(recent_gaps) - recent_gaps[0]
    if best_improvement >= STALL_MIN_IMPROVEMENT:
        return False

    # Gap is flat — but if the pool is still shrinking, the engine is making progress
    if pool_history is not None and len(pool_history) >= STALL_WINDOW:
        recent_pools = pool_history[-STALL_WINDOW:]
        if recent_pools[-1] < recent_pools[0]:
            return False

    return True


def should_guess(
    ranked_entities: list[tuple[Entity, float]],
    gap_history: list[float] | None = None,
    pool_history: list[int] | None = None,
) -> bool:
    if not ranked_entities:
        return False
    if len(ranked_entities) == 1:
        return True
    if len(ranked_entities) >= 2:
        gap = ranked_entities[0][1] - ranked_entities[1][1]
        if gap >= SCORE_GAP_THRESHOLD:
            return True
    if gap_history is not None and _is_stalled(gap_history, pool_history):
        return True
    return False


def next_action(
    questions: list[Question],
    entities: list[Entity],
    asked_question_ids: set[str],
    answers: dict[str, str],
    question_count: int,
    gap_history: list[float] | None = None,
    pool_history: list[int] | None = None,
) -> dict:
    """Returns {"action": "ask", "question": Question} or {"action": "guess", "entity": Entity, "ranked": [...]}."""
    ranked = rank_entities(entities, answers)
    remaining = len(ranked)

    if should_guess(ranked, gap_history, pool_history):
        return {
            "action": "guess",
            "entity": ranked[0][0],
            "ranked": ranked,
            "remaining_candidates": remaining,
        }

    question = select_next_question(
        questions,
        asked_question_ids,
        answered_attribute_keys=set(answers.keys()),
        ranked_entities=ranked,
        answers=answers,
        entities_all=entities,
    )

    if question is None:
        return {
            "action": "guess",
            "entity": ranked[0][0] if ranked else None,
            "ranked": ranked,
            "remaining_candidates": remaining,
        }

    return {
        "action": "ask",
        "question": question,
        "ranked": ranked,
        "remaining_candidates": remaining,
    }
