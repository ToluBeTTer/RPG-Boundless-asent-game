import tempfile
import unittest
from pathlib import Path

from boundless_ascent.character import Character, Race, Trait
from boundless_ascent.persistence import load_character, save_character


class PersistenceTests(unittest.TestCase):
    def test_save_and_load_character(self):
        c = Character(name="Saver", race=Race.CELESTIAL_BORN, trait=Trait.IRON_MEMORY)
        c.gain_xp(250)
        c.train_soul(3)

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "char.json"
            save_character(c, path)
            loaded = load_character(path)

        self.assertEqual(loaded.name, c.name)
        self.assertEqual(loaded.level, c.level)
        self.assertEqual(loaded.power_layers.soul_aether, c.power_layers.soul_aether)


if __name__ == "__main__":
    unittest.main()
