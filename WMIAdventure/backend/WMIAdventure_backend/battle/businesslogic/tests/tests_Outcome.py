from django.test import TestCase

from .Creator import Creator
from ..Deck import Deck
from ..Outcome import Outcome
from ..Player import Player


class OutcomeTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.creator = Creator()

        cls.user_profile_model1, cls.user_profile_model2 = \
            cls.creator.get_user_profile_models()

        cls.attacker_deck_model, cls.defender_deck_model = cls.creator.get_decks(1)

        cls.attacker = Player(cls.user_profile_model1.user.id,
                              Deck(cls.attacker_deck_model))

        cls.defender = Player(cls.user_profile_model2.user.id,
                              Deck(cls.defender_deck_model))

    def setUp(self) -> None:
        self.outcome = Outcome(self.attacker, self.defender)

    def test_creation(self):
        expected_attacker = self.attacker
        expected_defender = self.defender

        self.assertFalse(self.outcome.is_completed)
        self.assertIs(self.outcome.attacker, expected_attacker)
        self.assertIs(self.outcome.defender, expected_defender)

    def test_is_done_after_creation(self):
        self.assertFalse(self.outcome.is_done())

    def test_get_winner_after_creation(self):
        expected_outcome = None

        self.assertEqual(self.outcome.get_winner(), expected_outcome)

    def test_get_winner1(self):
        """
        Scenario: Defender is defeated.
        Expected result: Attacker is winner.
        """

        self.outcome.defender.statistics.hp = 0.0
        self.outcome.is_done()
        self.assertIs(self.outcome.get_winner(), self.attacker)

        # Restoring defender hp
        self.outcome.defender.statistics.hp = self.outcome.defender.statistics.MAX_HP

    def test_get_winner2(self):
        """
        Scenario: Attacker is defeated.
        Expected result: Defender is winner.
        """

        self.outcome.attacker.statistics.hp = 0.0
        self.outcome.is_done()
        self.assertIs(self.outcome.get_winner(), self.defender)

        # Restoring attacker hp
        self.outcome.attacker.statistics.hp = self.outcome.attacker.statistics.MAX_HP

    def test_get_winner3(self):
        """
        Scenario: Attacker and defender are defeated.
        Expected result: None is winner.
        """

        self.outcome.attacker.statistics.hp = 0.0
        self.outcome.defender.statistics.hp = 0.0

        self.outcome.is_done()
        self.assertIsNone(self.outcome.get_winner())

        # Restoring players hp
        self.outcome.attacker.statistics.hp = self.outcome.attacker.statistics.MAX_HP
        self.outcome.defender.statistics.hp = self.outcome.defender.statistics.MAX_HP

    @classmethod
    def tearDownClass(cls):
        cls.creator.perform_deletion()
