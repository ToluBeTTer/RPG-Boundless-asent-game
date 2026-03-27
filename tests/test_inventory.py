import unittest

from boundless_ascent.items import Inventory, Item, ItemType


class InventoryTests(unittest.TestCase):
    def test_add_equip_use_items(self):
        inv = Inventory()
        weapon = Item("w1", "W1", ItemType.WEAPON, power=4)
        potion = Item("p1", "Potion", ItemType.CONSUMABLE, heal=20, stackable=True)
        inv.add_item(weapon)
        inv.add_item(potion, 2)
        self.assertTrue(inv.equip("w1"))
        self.assertEqual(inv.weapon_power, 4)
        used = inv.use("p1")
        self.assertIsNotNone(used)
        self.assertEqual(inv.items["p1"], 1)


if __name__ == "__main__":
    unittest.main()
