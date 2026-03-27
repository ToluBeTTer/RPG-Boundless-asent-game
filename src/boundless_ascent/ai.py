from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .character import Character
from .combat import CombatEngine, CombatResult


class EnemyBehavior(str, Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    BALANCED = "balanced"


@dataclass
class EnemyController:
    behavior: EnemyBehavior = EnemyBehavior.BALANCED

    def choose_action(self, enemy: Character) -> str:
        low_hp = enemy.hp < 35
        low_stamina = enemy.stamina < 10

        if self.behavior == EnemyBehavior.AGGRESSIVE:
            if low_stamina:
                return "recover"
            return "attack"

        if self.behavior == EnemyBehavior.DEFENSIVE:
            if low_hp or low_stamina:
                return "recover"
            return "attack"

        # balanced
        if low_stamina:
            return "recover"
        if low_hp and enemy.stamina >= 10:
            return "recover"
        return "attack"


@dataclass
class EncounterOutcome:
    rounds: int
    winner: str


class EncounterEngine:
    def __init__(self, enemy_controller: EnemyController | None = None):
        self.enemy_controller = enemy_controller or EnemyController()

    def run_duel(self, player: Character, enemy: Character, max_rounds: int = 50) -> EncounterOutcome:
        rounds = 0
        while player.hp > 0 and enemy.hp > 0 and rounds < max_rounds:
            rounds += 1
            self._safe_basic_attack(player, enemy)
            if enemy.hp <= 0:
                break

            action = self.enemy_controller.choose_action(enemy)
            if action == "recover":
                enemy.stamina = min(100, enemy.stamina + 8)
            else:
                self._safe_basic_attack(enemy, player)

        winner = player.name if player.hp > 0 and enemy.hp <= 0 else enemy.name
        return EncounterOutcome(rounds=rounds, winner=winner)

    @staticmethod
    def _safe_basic_attack(attacker: Character, defender: Character) -> CombatResult | None:
        try:
            return CombatEngine.basic_attack(attacker, defender)
        except ValueError:
            attacker.stamina = min(100, attacker.stamina + 6)
            return None
