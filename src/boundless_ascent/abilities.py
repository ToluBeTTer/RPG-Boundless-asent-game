from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .character import Character


class MoveType(str, Enum):
    DASH = "dash"
    PROJECTILE = "projectile"
    AOE = "aoe"
    GRAB = "grab"
    BUFF = "buff"
    SUMMON = "summon"
    DOMAIN = "domain"


class EnergyLayer(str, Enum):
    VITAL = "vital"
    SOUL = "soul"
    ORIGIN = "origin"


@dataclass(frozen=True)
class AbilityBlueprint:
    name: str
    move_type: MoveType
    energy_layer: EnergyLayer
    element: str
    range_score: int = 1
    size_score: int = 1
    charge_score: int = 1


@dataclass(frozen=True)
class Ability:
    blueprint: AbilityBlueprint
    power: int
    essence_cost: int
    stamina_cost: int


class AbilityBuilder:
    @staticmethod
    def point_budget(character: Character) -> int:
        return 8 + character.level // 2 + character.stats.control // 5

    @classmethod
    def build(cls, character: Character, blueprint: AbilityBlueprint) -> Ability:
        budget = cls.point_budget(character)
        cost = blueprint.range_score + blueprint.size_score + blueprint.charge_score
        if cost > budget:
            raise ValueError(f"Blueprint exceeds point budget: cost={cost}, budget={budget}")

        layer_power = {
            EnergyLayer.VITAL: character.power_layers.vital_aether,
            EnergyLayer.SOUL: character.power_layers.soul_aether,
            EnergyLayer.ORIGIN: max(1, character.power_layers.origin_flame),
        }[blueprint.energy_layer]

        base = character.stats.essence + character.stats.control + layer_power * 2
        power = base + (blueprint.range_score * blueprint.size_score)
        essence_cost = max(5, cost * 3)
        stamina_cost = max(3, blueprint.charge_score * 2)
        return Ability(blueprint=blueprint, power=power, essence_cost=essence_cost, stamina_cost=stamina_cost)
