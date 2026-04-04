from .models import Entity


def filter_entities(entities: list[Entity], answers: dict[str, str]) -> list[Entity]:
    filtered_entities: list[Entity] = []

    for entity in entities:
        keep_entity = True

        for attribute_key, answer in answers.items():
            attribute_value = entity.attributes.get(attribute_key, 0.5)

            if answer == "yes" and attribute_value < 0.25:
                keep_entity = False
                break

            if answer == "no" and attribute_value > 0.75:
                keep_entity = False
                break

        if keep_entity:
            filtered_entities.append(entity)

    return filtered_entities
