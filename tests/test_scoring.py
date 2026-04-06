import unittest

from packages.engine.models import Entity
from packages.engine.scoring import ANSWER_WEIGHTS, score_entity


def _entity(id: str, **attrs: float) -> Entity:
    return Entity(id=id, name=id, attributes=attrs)


class TestAnswerWeights(unittest.TestCase):
    def test_weight_values(self) -> None:
        self.assertEqual(ANSWER_WEIGHTS["yes"], 1.0)
        self.assertEqual(ANSWER_WEIGHTS["probably_yes"], 0.75)
        self.assertEqual(ANSWER_WEIGHTS["i_dont_know"], 0.5)
        self.assertEqual(ANSWER_WEIGHTS["probably_no"], 0.25)
        self.assertEqual(ANSWER_WEIGHTS["no"], 0.0)


class TestScoreEntity(unittest.TestCase):
    # --- perfect match ---

    def test_perfect_yes_match(self) -> None:
        ent = _entity("a", is_female=1.0)
        score = score_entity(ent, {"is_female": "yes"})
        # 1.0 - abs(1.0 - 1.0) = 1.0
        self.assertAlmostEqual(score, 1.0)

    def test_perfect_no_match(self) -> None:
        ent = _entity("a", is_female=0.0)
        score = score_entity(ent, {"is_female": "no"})
        # 1.0 - abs(0.0 - 0.0) = 1.0
        self.assertAlmostEqual(score, 1.0)

    # --- complete mismatch ---

    def test_total_mismatch_yes(self) -> None:
        ent = _entity("a", is_female=0.0)
        score = score_entity(ent, {"is_female": "yes"})
        # 1.0 - abs(1.0 - 0.0) = 0.0
        self.assertAlmostEqual(score, 0.0)

    def test_total_mismatch_no(self) -> None:
        ent = _entity("a", is_female=1.0)
        score = score_entity(ent, {"is_female": "no"})
        # 1.0 - abs(0.0 - 1.0) = 0.0
        self.assertAlmostEqual(score, 0.0)

    # --- score accumulation across multiple answers ---

    def test_scores_accumulate(self) -> None:
        ent = _entity("a", is_female=1.0, is_musician=1.0)
        score = score_entity(ent, {"is_female": "yes", "is_musician": "yes"})
        # 1.0 + 1.0 = 2.0
        self.assertAlmostEqual(score, 2.0)

    def test_mixed_match_accumulation(self) -> None:
        ent = _entity("a", is_female=1.0, is_musician=0.0)
        score = score_entity(ent, {"is_female": "yes", "is_musician": "yes"})
        # 1.0 + 0.0 = 1.0
        self.assertAlmostEqual(score, 1.0)

    # --- missing attribute defaults to 0.5 ---

    def test_missing_attribute_uses_neutral(self) -> None:
        ent = _entity("a")  # no attributes
        score = score_entity(ent, {"is_female": "yes"})
        # 1.0 - abs(1.0 - 0.5) = 0.5
        self.assertAlmostEqual(score, 0.5)

    def test_missing_attribute_with_no_answer(self) -> None:
        ent = _entity("a")
        score = score_entity(ent, {"is_female": "no"})
        # 1.0 - abs(0.0 - 0.5) = 0.5
        self.assertAlmostEqual(score, 0.5)

    # --- unknown answer string defaults to 0.5 ---

    def test_unknown_answer_defaults_to_neutral(self) -> None:
        ent = _entity("a", is_female=1.0)
        score = score_entity(ent, {"is_female": "garbage"})
        # 1.0 - abs(0.5 - 1.0) = 0.5
        self.assertAlmostEqual(score, 0.5)

    # --- empty answers ---

    def test_no_answers_gives_zero(self) -> None:
        ent = _entity("a", is_female=1.0)
        score = score_entity(ent, {})
        self.assertAlmostEqual(score, 0.0)

    # --- fuzzy attribute values ---

    def test_fuzzy_attribute_value(self) -> None:
        ent = _entity("a", is_female=0.7)
        score = score_entity(ent, {"is_female": "yes"})
        # 1.0 - abs(1.0 - 0.7) = 0.7
        self.assertAlmostEqual(score, 0.7)

    # --- ranking order ---

    def test_better_match_scores_higher(self) -> None:
        perfect = _entity("a", is_female=1.0, is_musician=1.0)
        partial = _entity("b", is_female=1.0, is_musician=0.0)
        answers = {"is_female": "yes", "is_musician": "yes"}
        self.assertGreater(
            score_entity(perfect, answers), score_entity(partial, answers)
        )


if __name__ == "__main__":
    unittest.main()
