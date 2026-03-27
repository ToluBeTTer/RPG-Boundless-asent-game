from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .character import Character


class QuestStatus(str, Enum):
    LOCKED = "locked"
    ACTIVE = "active"
    COMPLETED = "completed"


@dataclass
class QuestObjective:
    key: str
    target: int
    progress: int = 0

    @property
    def complete(self) -> bool:
        return self.progress >= self.target


@dataclass
class QuestReward:
    xp: int = 0
    stat_boost: int = 0


@dataclass
class Quest:
    quest_id: str
    title: str
    objectives: list[QuestObjective]
    reward: QuestReward
    status: QuestStatus = QuestStatus.LOCKED

    @property
    def is_complete(self) -> bool:
        return all(obj.complete for obj in self.objectives)


@dataclass
class QuestLog:
    quests: dict[str, Quest] = field(default_factory=dict)

    def add_quest(self, quest: Quest, activate: bool = True) -> None:
        quest.status = QuestStatus.ACTIVE if activate else QuestStatus.LOCKED
        self.quests[quest.quest_id] = quest

    def record_event(self, event_key: str, value: int = 1) -> list[Quest]:
        completed: list[Quest] = []
        for quest in self.quests.values():
            if quest.status != QuestStatus.ACTIVE:
                continue
            for objective in quest.objectives:
                if objective.key == event_key and not objective.complete:
                    objective.progress += value
            if quest.is_complete:
                quest.status = QuestStatus.COMPLETED
                completed.append(quest)
        return completed

    def apply_rewards(self, character: Character, completed_quests: list[Quest]) -> None:
        for quest in completed_quests:
            character.gain_xp(quest.reward.xp)
            character.stats.strength += quest.reward.stat_boost
            character.stats.agility += quest.reward.stat_boost
