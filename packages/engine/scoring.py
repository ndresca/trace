from .models import Entity


ANSWER_WEIGHTS: dict[str, float] = {
    "yes": 1.0,
    "probably_yes": 0.75,
    "i_dont_know": 0.5,
    "probably_no": 0.25,
    "no": 0.0,
}


def score_entity(entity: Entity, answers: dict[str, str]) -> float:
    score = 0.0

    for attribute_key, answer in answers.items():
        answer_value = ANSWER_WEIGHTS.get(answer, 0.5)
        attribute_value = entity.attributes.get(attribute_key, 0.5)
        contribution = 1.0 - abs(answer_value - attribute_value)
        score += contribution

    return score
