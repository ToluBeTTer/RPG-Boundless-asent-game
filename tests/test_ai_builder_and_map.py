import unittest

from boundless_ascent.ai_builder import AICharacterBuilder
from boundless_ascent.gameplay import GameRuntime


class AIBuilderAndMapTests(unittest.TestCase):
    def test_ai_builder_generates_build(self):
        generated = AICharacterBuilder.from_description(
            name="Astra",
            description="shadow lightning assassin swordsman",
        )
        self.assertGreaterEqual(len(generated.abilities), 1)
        self.assertIn("AI generated", generated.summary)

    def test_runtime_map_generation(self):
        game = GameRuntime(seed=1)
        zone_map = game.zone_map()
        self.assertIn("\n", zone_map)
        self.assertGreater(len(zone_map.splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
