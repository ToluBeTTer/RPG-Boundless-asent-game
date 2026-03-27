import unittest

from boundless_ascent.gameplay import GameRuntime
from boundless_ascent_cli import execute_command


class CLISessionTests(unittest.TestCase):
    def test_profile_help_and_atlas(self):
        game = GameRuntime(seed=1)
        game, help_out = execute_command(game, "help")
        self.assertIn("atlas", help_out)
        game, profile_out = execute_command(game, "profile")
        self.assertIn("lvl", profile_out)
        game, atlas = execute_command(game, "atlas")
        self.assertIn("landmarks", atlas)

    def test_ai_create_and_world_actions(self):
        game = GameRuntime(seed=1)
        game, created = execute_command(game, "create Nova|shadow assassin swordsman")
        self.assertIn("Created AI build", created)
        game, _ = execute_command(game, "quest-board")
        game, landmarks = execute_command(game, "landmarks")
        self.assertIn("Village", landmarks)
        game, _ = execute_command(game, "party-create alpha")
        game, _ = execute_command(game, "say hello world")
        game, chat = execute_command(game, "chat")
        self.assertIn("hello world", chat)


if __name__ == "__main__":
    unittest.main()
