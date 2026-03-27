from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Material:
    name: str
    weight: int
    durability: int
    resonance: str


@dataclass
class Weapon:
    name: str
    attack: int
    speed: int
    durability: int
    resonances: set[str] = field(default_factory=set)


@dataclass
class Armor:
    name: str
    defense: int
    durability: int
    resonances: set[str] = field(default_factory=set)


class CraftingEngine:
    @staticmethod
    def craft_weapon(name: str, materials: Iterable[Material]) -> Weapon:
        mats = list(materials)
        if not mats:
            raise ValueError("At least one material is required")
        attack = sum(m.weight for m in mats) + len(mats) * 2
        speed = max(1, 20 - sum(m.weight for m in mats) // 2)
        durability = sum(m.durability for m in mats)
        resonances = {m.resonance for m in mats}
        return Weapon(name=name, attack=attack, speed=speed, durability=durability, resonances=resonances)

    @staticmethod
    def craft_armor(name: str, materials: Iterable[Material]) -> Armor:
        mats = list(materials)
        if not mats:
            raise ValueError("At least one material is required")
        defense = sum(m.durability for m in mats) // 2 + len(mats)
        durability = sum(m.durability for m in mats)
        resonances = {m.resonance for m in mats}
        return Armor(name=name, defense=defense, durability=durability, resonances=resonances)

    @staticmethod
    def fuse_weapons(name: str, primary: Weapon, secondary: Weapon) -> Weapon:
        return Weapon(
            name=name,
            attack=round(primary.attack * 0.7 + secondary.attack * 0.45),
            speed=max(1, round(primary.speed * 0.65 + secondary.speed * 0.35)),
            durability=round(primary.durability * 0.6 + secondary.durability * 0.5),
            resonances=primary.resonances | secondary.resonances,
        )

    @staticmethod
    def fuse_armor(name: str, primary: Armor, secondary: Armor) -> Armor:
        return Armor(
            name=name,
            defense=round(primary.defense * 0.7 + secondary.defense * 0.45),
            durability=round(primary.durability * 0.6 + secondary.durability * 0.5),
            resonances=primary.resonances | secondary.resonances,
        )
