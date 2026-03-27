from __future__ import annotations

from dataclasses import dataclass

from .abilities import Ability
from .character import Character


@dataclass
class CombatResult:
    attacker: str
    defender: str
    damage: int
    defender_hp_after: int
    used_ability: str | None = None


class CombatEngine:
    @staticmethod
    def basic_attack(attacker: Character, defender: Character) -> CombatResult:
        if not attacker.spend_stamina(5):
            raise ValueError(f"{attacker.name} does not have enough stamina")
        damage = defender.apply_damage(attacker.attack_power)
        return CombatResult(attacker.name, defender.name, damage, defender.hp)

    @staticmethod
    def use_ability(attacker: Character, defender: Character, ability: Ability) -> CombatResult:
        if not attacker.spend_stamina(ability.stamina_cost):
            raise ValueError(f"{attacker.name} does not have enough stamina")
        if not attacker.spend_essence(ability.essence_cost):
            raise ValueError(f"{attacker.name} does not have enough essence")

        damage = defender.apply_damage(ability.power + attacker.stats.essence)
        return CombatResult(attacker.name, defender.name, damage, defender.hp, used_ability=ability.blueprint.name)
