from __future__ import annotations

import json
import random
from pathlib import Path

from .models import Entity, Question


_EXCLUSION_GROUPS_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data" / "questions" / "exclusion_groups_v1.json"
)

_exclusion_groups_cache: dict[str, list[str]] | None = None


def _load_exclusion_groups() -> dict[str, list[str]]:
    global _exclusion_groups_cache
    if _exclusion_groups_cache is None:
        with _EXCLUSION_GROUPS_PATH.open("r", encoding="utf-8") as f:
            _exclusion_groups_cache = json.load(f)
    return _exclusion_groups_cache


# Domain-specific attributes: questions that discriminate WITHIN a domain.
DOMAIN_ATTRIBUTES: dict[str, set[str]] = {
    "is_musician": {
        "is_singer", "is_rapper", "is_band_member", "has_won_grammy",
        "is_pop_star", "known_by_single_name", "uses_stage_name",
    },
    "is_actor": {
        "known_for_movies", "known_for_television", "known_for_superhero_role",
        "associated_with_marvel", "associated_with_disney", "has_won_oscar",
    },
    "is_athlete": {
        "plays_team_sport", "plays_solo_sport", "is_soccer_player",
        "is_basketball_player", "is_tennis_player", "is_racing_driver",
        "is_wrestler", "has_won_major_championship",
    },
    "is_politician": {
        "is_us_president", "is_head_of_state", "has_held_elected_office",
        "has_won_nobel_prize",
    },
    "is_internet_personality": {
        "known_for_reality_tv", "known_for_social_media", "known_for_streaming",
    },
}

# Primary domain classifiers: asked early to identify the target's domain
DOMAIN_CLASSIFIERS: set[str] = {
    "is_musician", "is_actor", "is_athlete", "is_politician", "is_internet_personality",
}

CLASSIFIER_BONUS = 0.05  # additive bonus subtracted from classifier scores (lower = better)
DOMAIN_BOOST = 0.5  # multiplier for sub-domain questions when domain is concentrated
DOMAIN_THRESHOLD = 0.6  # >60% of pool must share a domain to activate sub-domain boost
JITTER_AMOUNT = 0.02  # random noise to break ties and vary question order across games

# Opener attributes: boosted on the very first question to ensure a broad,
# high-signal split before narrowing into domains or geography.
OPENER_ATTRIBUTES: set[str] = {"is_female"}
OPENER_BONUS = 0.05  # additive bonus (subtracted from score, lower = better)


def _detect_dominant_domain(
    entities: list[Entity],
) -> str | None:
    """Return the domain key if >60% of entities belong to one domain."""
    if not entities:
        return None
    n = len(entities)
    for domain_key in DOMAIN_ATTRIBUTES:
        count = sum(
            1 for e in entities if e.attributes.get(domain_key, 0.0) >= 0.75
        )
        if count / n > DOMAIN_THRESHOLD:
            return domain_key
    return None


def _information_gain_score(
    question: Question,
    entities: list[Entity],
    dominant_domain: str | None,
    domain_confirmed: bool,
    is_first_question: bool = False,
) -> float:
    """Lower is better. Aligned with filtering thresholds (< 0.25 and > 0.75)."""
    values = [
        e.attributes.get(question.attribute_key, 0.5) for e in entities
    ]
    n = len(values)
    if n == 0:
        return 1.0

    # Count entities that would be eliminated by each answer
    elim_if_yes = sum(1 for v in values if v < 0.25)
    elim_if_no = sum(1 for v in values if v > 0.75)

    # Split quality: product of elimination fractions (max 0.25 at perfect 50/50)
    split_quality = (elim_if_yes * elim_if_no) / (n * n)

    # Convert to lower-is-better (0.0 = perfect 50/50 split, 0.25 = no split)
    score = 0.25 - split_quality

    # Boost opener attributes on the very first question
    if is_first_question and question.attribute_key in OPENER_ATTRIBUTES:
        score -= OPENER_BONUS

    # Boost classifiers only BEFORE a domain is confirmed
    if not domain_confirmed and question.attribute_key in DOMAIN_CLASSIFIERS:
        score -= CLASSIFIER_BONUS

    # Boost sub-domain questions when the pool is domain-concentrated
    if dominant_domain is not None:
        if question.attribute_key in DOMAIN_ATTRIBUTES[dominant_domain]:
            score *= DOMAIN_BOOST

    return score


def select_next_question(
    questions: list[Question],
    asked_question_ids: set[str],
    answered_attribute_keys: set[str] | None = None,
    ranked_entities: list[tuple[Entity, float]] | None = None,
    answers: dict[str, str] | None = None,
    entities_all: list[Entity] | None = None,
) -> Question | None:
    excluded_attribute_keys: set[str] = set()

    if answers is not None:
        for attribute_key, answer in answers.items():
            if answer == "yes":
                excluded_attribute_keys.update(
                    _load_exclusion_groups().get(attribute_key, [])
                )

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
        entities = [entity for entity, _ in ranked_entities]
    else:
        entities = entities_all or []

    if entities:
        dominant_domain = _detect_dominant_domain(entities)
        is_first = not asked_question_ids

        # Stop boosting classifiers once a domain is confirmed (yes answer)
        domain_confirmed = False
        if answers:
            for dk in DOMAIN_CLASSIFIERS:
                if answers.get(dk) == "yes":
                    domain_confirmed = True
                    break

        return min(
            remaining_questions,
            key=lambda q: (
                _information_gain_score(
                    q, entities, dominant_domain, domain_confirmed,
                    is_first_question=is_first,
                )
                + random.uniform(0, JITTER_AMOUNT)
            ),
        )

    return max(remaining_questions, key=lambda question: question.priority)
