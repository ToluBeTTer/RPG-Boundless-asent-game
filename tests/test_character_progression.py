import unittest

from boundless_ascent.character import Character, Race, Trait


class CharacterProgressionTests(unittest.TestCase):
    def test_gain_xp_levels_up(self):
        c = Character(name="Test", race=Race.HUMAN, trait=Trait.PERCEPTIVE)
        leveled = c.gain_xp(125)
        self.assertTrue(leveled)
        self.assertEqual(c.level, 2)

    def test_origin_requires_threshold(self):
        c = Character(name="Test", race=Race.HUMAN, trait=Trait.PERCEPTIVE)
        self.assertFalse(c.awaken_origin())
        c.level = 10
        c.power_layers.vital_aether = 10
        c.power_layers.soul_aether = 10
        self.assertTrue(c.awaken_origin())
        self.assertEqual(c.power_layers.origin_flame, 1)


if __name__ == "__main__":
    unittest.main()
