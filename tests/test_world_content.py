import unittest

from boundless_ascent.content import generate_world_content


class WorldContentTests(unittest.TestCase):
    def test_content_has_landmarks_npcs_dungeons(self):
        content = generate_world_content(["Verdant Frontier"], seed=1)
        region = content.region("Verdant Frontier")
        self.assertGreaterEqual(len(region.landmarks), 3)
        self.assertGreaterEqual(len(region.npcs), 1)
        self.assertGreaterEqual(len(region.dungeons), 1)


if __name__ == "__main__":
    unittest.main()
