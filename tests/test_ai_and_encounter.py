import unittest

from boundless_ascent.ai import EncounterEngine, EnemyBehavior, EnemyController
from boundless_ascent.character import Character, Race, Trait


class AIEncounterTests(unittest.TestCase):
    def test_defensive_enemy_recovers_when_low(self):
        enemy = Character(name="Enemy", race=Race.VOID_MARKED, trait=Trait.RELENTLESS, hp=20, stamina=5)
        controller = EnemyController(behavior=EnemyBehavior.DEFENSIVE)
        action = controller.choose_action(enemy)
        self.assertEqual(action, "recover")

    def test_encounter_completes_with_winner(self):
        player = Character(name="Player", race=Race.HUMAN, trait=Trait.PERCEPTIVE)
        enemy = Character(name="Enemy", race=Race.VOID_MARKED, trait=Trait.RELENTLESS, hp=60)
        outcome = EncounterEngine().run_duel(player, enemy)
        self.assertIn(outcome.winner, {"Player", "Enemy"})
        self.assertGreater(outcome.rounds, 0)


if __name__ == "__main__":
    unittest.main()
