import unittest

from packages.engine.models import Entity, Question
from packages.engine.selection import select_next_question, _load_exclusion_groups


def _entity(id: str, **attrs: float) -> Entity:
    return Entity(id=id, name=id, attributes=attrs)


def _question(id: str, attr: str, priority: int = 0, enabled: bool = True) -> Question:
    return Question(id=id, text=f"Is {attr}?", attribute_key=attr, priority=priority, enabled=enabled)


class TestSelectNextQuestion(unittest.TestCase):
    def setUp(self) -> None:
        self.questions = [
            _question("q1", "is_female", priority=10),
            _question("q2", "is_musician", priority=5),
            _question("q3", "is_actor", priority=1),
        ]

    # --- basic selection by priority (no rankings) ---

    def test_selects_highest_priority_without_rankings(self) -> None:
        q = select_next_question(self.questions, set())
        self.assertEqual(q.id, "q1")  # priority=10 is highest

    def test_skips_already_asked(self) -> None:
        q = select_next_question(self.questions, {"q1"})
        self.assertEqual(q.id, "q2")  # next highest priority

    def test_skips_already_answered_attributes(self) -> None:
        q = select_next_question(
            self.questions, set(), answered_attribute_keys={"is_female"}
        )
        self.assertEqual(q.id, "q2")

    def test_skips_disabled_questions(self) -> None:
        questions = [
            _question("q1", "is_female", priority=10, enabled=False),
            _question("q2", "is_musician", priority=5),
        ]
        q = select_next_question(questions, set())
        self.assertEqual(q.id, "q2")

    def test_returns_none_when_all_asked(self) -> None:
        q = select_next_question(self.questions, {"q1", "q2", "q3"})
        self.assertIsNone(q)

    def test_returns_none_when_empty_question_list(self) -> None:
        q = select_next_question([], set())
        self.assertIsNone(q)

    # --- spread-based selection with ranked entities ---

    def test_info_gain_picks_best_filter_split(self) -> None:
        # is_musician splits 2/2 (perfect), is_female splits 0/4 (useless)
        entities = [
            _entity("a", is_female=1.0, is_musician=1.0, is_actor=0.5),
            _entity("b", is_female=1.0, is_musician=1.0, is_actor=0.5),
            _entity("c", is_female=1.0, is_musician=0.0, is_actor=0.5),
            _entity("d", is_female=1.0, is_musician=0.0, is_actor=0.5),
        ]
        ranked = [(e, 1.0) for e in entities]

        q = select_next_question(self.questions, set(), ranked_entities=ranked)
        # is_musician: elim_yes=2, elim_no=2, product=0.25 → best split
        # is_female: elim_yes=0, elim_no=4, product=0 → no split
        self.assertEqual(q.attribute_key, "is_musician")

    def test_info_gain_uses_full_pool(self) -> None:
        # All entities in the ranked list contribute to the score
        entities = [
            _entity("a", is_female=1.0, is_musician=1.0),
            _entity("b", is_female=1.0, is_musician=0.0),
            _entity("c", is_female=0.0, is_musician=1.0),
            _entity("d", is_female=0.0, is_musician=0.0),
            _entity("e", is_female=0.0, is_musician=0.0),
            _entity("f", is_female=0.0, is_musician=0.0),
            _entity("g", is_female=0.0, is_musician=0.0),
        ]
        ranked = [(e, 7.0 - i) for i, e in enumerate(entities)]

        q = select_next_question(self.questions, set(), ranked_entities=ranked)
        # is_female: elim_yes=5, elim_no=2, product=10/49=0.204
        # is_musician: elim_yes=5, elim_no=2, product=10/49=0.204
        # Tied — verify it returns a valid question
        self.assertIsNotNone(q)

    def test_info_gain_ignores_zero_variance_attributes(self) -> None:
        # When no entity would be eliminated by either answer, question is useless
        entities = [
            _entity("a", is_female=0.5, is_musician=1.0),
            _entity("b", is_female=0.5, is_musician=0.0),
        ]
        ranked = [(e, 1.0) for e in entities]

        q = select_next_question(self.questions, set(), ranked_entities=ranked)
        # is_female: all at 0.5, elim_yes=0, elim_no=0 → product=0 → worst
        # is_musician: elim_yes=1, elim_no=1 → product=0.25 → perfect
        self.assertEqual(q.attribute_key, "is_musician")

    # --- exclusion group enforcement ---

    def test_exclusion_groups_exclude_contradicted_attributes(self) -> None:
        questions = [
            _question("q1", "plays_team_sport", priority=10),
            _question("q2", "plays_solo_sport", priority=5),
            _question("q3", "is_female", priority=1),
        ]
        # User said "yes" to team sport -> solo sport should be excluded
        q = select_next_question(
            questions,
            {"q1"},
            answered_attribute_keys={"plays_team_sport"},
            answers={"plays_team_sport": "yes"},
        )
        self.assertNotEqual(q.attribute_key, "plays_solo_sport")
        self.assertEqual(q.attribute_key, "is_female")

    def test_exclusion_only_triggers_on_yes(self) -> None:
        questions = [
            _question("q1", "plays_team_sport", priority=10),
            _question("q2", "plays_solo_sport", priority=5),
        ]
        # User said "no" to team sport -> solo sport should NOT be excluded
        q = select_next_question(
            questions,
            {"q1"},
            answered_attribute_keys={"plays_team_sport"},
            answers={"plays_team_sport": "no"},
        )
        self.assertEqual(q.attribute_key, "plays_solo_sport")

    def test_exclusion_groups_load_from_file(self) -> None:
        groups = _load_exclusion_groups()
        self.assertIn("is_real_person", groups)
        self.assertIn("is_fictional", groups["is_real_person"])


class TestEarlyExitConditions(unittest.TestCase):
    """Tests for early-exit logic as implemented in play_cli.py and run_eval.py.

    The engine itself doesn't implement early exit — it's in the game loop.
    These tests document the expected thresholds so they're pinned.
    """

    def test_score_gap_threshold(self) -> None:
        """Score gap >= 1.0 should trigger early guess."""
        from packages.engine.scoring import score_entity

        winner = _entity("a", is_female=1.0, is_musician=1.0)
        loser = _entity("b", is_female=0.0, is_musician=0.0)
        answers = {"is_female": "yes", "is_musician": "yes"}

        winner_score = score_entity(winner, answers)
        loser_score = score_entity(loser, answers)

        gap = winner_score - loser_score
        self.assertGreaterEqual(gap, 1.0, "Two yes answers on matching attrs should create >= 1.0 gap")

    def test_single_candidate_after_filtering(self) -> None:
        """When filtering leaves exactly one entity, the game should guess it."""
        from packages.engine.filtering import filter_entities

        entities = [
            _entity("a", is_female=1.0, is_musician=1.0),
            _entity("b", is_female=0.0, is_musician=1.0),
            _entity("c", is_female=1.0, is_musician=0.0),
        ]
        result = filter_entities(entities, {"is_female": "yes", "is_musician": "yes"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "a")


if __name__ == "__main__":
    unittest.main()
