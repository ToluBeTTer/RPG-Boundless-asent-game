import unittest

from boundless_ascent.gameplay import GameRuntime
from boundless_ascent.items import Item, ItemType


class GameplayLoopTests(unittest.TestCase):
    def test_explore_rewards_progress(self):
        game = GameRuntime(seed=1)
        before_gold = game.inventory.gold
        result = game.explore()
        self.assertIn("Defeated", result)
        self.assertGreaterEqual(game.inventory.gold, before_gold)

    def test_buy_and_equip(self):
        game = GameRuntime(seed=1)
        item = Item("test_blade", "Test Blade", ItemType.WEAPON, value=10, power=5)
        self.assertIn("Purchased", game.buy(item))
        self.assertIn("Equipped", game.equip_item("test_blade"))

    def test_world_content_actions(self):
        game = GameRuntime(seed=1)
        self.assertIn("landmarks", game.atlas())
        self.assertIn("Posted quests", game.post_local_quests())
        self.assertIn("Cleared", game.delve(1))
        self.assertIn("treasure", game.treasure_hunt().lower())


if __name__ == "__main__":
    unittest.main()
