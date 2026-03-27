import unittest

from boundless_ascent.character import Character, Race, Trait
from boundless_ascent.quests import Quest, QuestLog, QuestObjective, QuestReward, QuestStatus
from boundless_ascent.server import GameServerState


class QuestAndServerTests(unittest.TestCase):
    def test_quest_event_completion_and_rewards(self):
        character = Character(name="Hero", race=Race.HUMAN, trait=Trait.PERCEPTIVE)
        log = QuestLog()
        log.add_quest(
            Quest(
                quest_id="hunt_01",
                title="Defeat Slimes",
                objectives=[QuestObjective("slime_defeated", 2)],
                reward=QuestReward(xp=100, stat_boost=1),
            )
        )
        completed = log.record_event("slime_defeated", 2)
        log.apply_rewards(character, completed)

        self.assertEqual(len(completed), 1)
        self.assertEqual(log.quests["hunt_01"].status, QuestStatus.COMPLETED)
        self.assertGreaterEqual(character.level, 2)

    def test_server_state_tick_and_commands(self):
        server = GameServerState()
        char = Character(name="Net", race=Race.HUMAN, trait=Trait.RESONANT_SOUL)
        server.connect_player("p1", char)
        server.apply_command("p1", "move", {"dx": 3, "dy": -2})
        server.apply_command("p1", "attack")
        pre_tick = server.state.tick
        server.tick()

        session = server.state.sessions["p1"]
        self.assertEqual((session.x, session.y), (3, -2))
        self.assertEqual(server.state.tick, pre_tick + 1)


if __name__ == "__main__":
    unittest.main()
