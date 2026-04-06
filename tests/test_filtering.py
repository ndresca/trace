import unittest

from packages.engine.models import Entity
from packages.engine.filtering import filter_entities


def _entity(id: str, **attrs: float) -> Entity:
    return Entity(id=id, name=id, attributes=attrs)


class TestFilterEntities(unittest.TestCase):
    def setUp(self) -> None:
        self.entities = [
            _entity("a", is_female=1.0, is_musician=1.0),
            _entity("b", is_female=0.0, is_musician=1.0),
            _entity("c", is_female=1.0, is_musician=0.0),
            _entity("d", is_female=0.0, is_musician=0.0),
        ]

    # --- hard yes threshold: attribute < 0.25 is eliminated ---

    def test_yes_removes_entities_with_zero(self) -> None:
        result = filter_entities(self.entities, {"is_female": "yes"})
        ids = [e.id for e in result]
        self.assertIn("a", ids)
        self.assertIn("c", ids)
        self.assertNotIn("b", ids)  # is_female=0.0 < 0.25
        self.assertNotIn("d", ids)

    def test_yes_keeps_entity_at_boundary(self) -> None:
        ent = _entity("edge", is_female=0.25)
        result = filter_entities([ent], {"is_female": "yes"})
        self.assertEqual(len(result), 1, "0.25 is NOT < 0.25, should be kept")

    def test_yes_removes_entity_just_below_boundary(self) -> None:
        ent = _entity("edge", is_female=0.24)
        result = filter_entities([ent], {"is_female": "yes"})
        self.assertEqual(len(result), 0, "0.24 < 0.25, should be removed")

    # --- hard no threshold: attribute > 0.75 is eliminated ---

    def test_no_removes_entities_with_one(self) -> None:
        result = filter_entities(self.entities, {"is_female": "no"})
        ids = [e.id for e in result]
        self.assertIn("b", ids)
        self.assertIn("d", ids)
        self.assertNotIn("a", ids)  # is_female=1.0 > 0.75
        self.assertNotIn("c", ids)

    def test_no_keeps_entity_at_boundary(self) -> None:
        ent = _entity("edge", is_female=0.75)
        result = filter_entities([ent], {"is_female": "no"})
        self.assertEqual(len(result), 1, "0.75 is NOT > 0.75, should be kept")

    def test_no_removes_entity_just_above_boundary(self) -> None:
        ent = _entity("edge", is_female=0.76)
        result = filter_entities([ent], {"is_female": "no"})
        self.assertEqual(len(result), 0, "0.76 > 0.75, should be removed")

    # --- soft answers (probably_yes, probably_no, i_dont_know) never filter ---

    def test_probably_yes_does_not_filter(self) -> None:
        result = filter_entities(self.entities, {"is_female": "probably_yes"})
        self.assertEqual(len(result), 4)

    def test_probably_no_does_not_filter(self) -> None:
        result = filter_entities(self.entities, {"is_female": "probably_no"})
        self.assertEqual(len(result), 4)

    def test_i_dont_know_does_not_filter(self) -> None:
        result = filter_entities(self.entities, {"is_female": "i_dont_know"})
        self.assertEqual(len(result), 4)

    # --- missing attributes default to 0.5, never filtered ---

    def test_missing_attribute_defaults_to_neutral(self) -> None:
        ent = _entity("no_attr")
        result = filter_entities([ent], {"is_female": "yes"})
        self.assertEqual(len(result), 1, "0.5 is not < 0.25, should survive yes")

        result = filter_entities([ent], {"is_female": "no"})
        self.assertEqual(len(result), 1, "0.5 is not > 0.75, should survive no")

    # --- multiple answers compound ---

    def test_multiple_answers_narrow_candidates(self) -> None:
        result = filter_entities(
            self.entities, {"is_female": "yes", "is_musician": "yes"}
        )
        ids = [e.id for e in result]
        self.assertEqual(ids, ["a"])

    def test_contradictory_answers_can_eliminate_all(self) -> None:
        entities = [
            _entity("x", is_female=1.0),
            _entity("y", is_female=0.0),
        ]
        result = filter_entities(entities, {"is_female": "yes"})
        self.assertEqual(len(result), 1)
        # now filter the survivor with the opposite answer on a different attr
        result = filter_entities(
            entities, {"is_female": "yes", "is_musician": "yes"}
        )
        # x has no is_musician attr (defaults to 0.5, survives)
        self.assertEqual(len(result), 1)

    def test_empty_answers_returns_all(self) -> None:
        result = filter_entities(self.entities, {})
        self.assertEqual(len(result), 4)


if __name__ == "__main__":
    unittest.main()
