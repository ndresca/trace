from .models import Entity


ANSWER_WEIGHTS: dict[str, float] = {
    "yes": 1.0,
    "probably_yes": 0.5,
    "i_dont_know": 0.0,
    "probably_no": -0.5,
    "no": -1.0,
}


def score_entity(entity: Entity, answers: dict[str, str]) -> float:
    score = 0.0

    for attribute_key, answer in answers.items():
        weight = ANSWER_WEIGHTS.get(answer, 0.0)
        attribute_value = entity.attributes.get(attribute_key, 0.0)
        score += attribute_value * weight

    return score
