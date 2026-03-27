from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .items import Item, ItemType


@dataclass
class EnemyTemplate:
    enemy_id: str
    name: str
    zone: str
    hp: int
    attack: int
    defense: int
    xp_reward: int
    gold_reward: int
    drops: list[Item]


ENEMY_TABLE: list[EnemyTemplate] = [
    EnemyTemplate(
        enemy_id="slime",
        name="Verdant Slime",
        zone="Verdant Frontier",
        hp=40,
        attack=8,
        defense=2,
        xp_reward=35,
        gold_reward=8,
        drops=[Item("slime_core", "Slime Core", ItemType.MATERIAL, value=12)],
    ),
    EnemyTemplate(
        enemy_id="wolf",
        name="Highland Wolf",
        zone="Highland Ruins",
        hp=65,
        attack=12,
        defense=4,
        xp_reward=55,
        gold_reward=14,
        drops=[Item("wolf_fang", "Wolf Fang", ItemType.MATERIAL, value=18)],
    ),
    EnemyTemplate(
        enemy_id="shade",
        name="Cursed Shade",
        zone="Cursed Marshlands",
        hp=90,
        attack=16,
        defense=6,
        xp_reward=80,
        gold_reward=20,
        drops=[Item("shade_essence", "Shade Essence", ItemType.MATERIAL, value=24)],
    ),
]


def roll_enemy(zone: str, rng: Random) -> EnemyTemplate:
    candidates = [e for e in ENEMY_TABLE if e.zone == zone]
    if not candidates:
        candidates = [ENEMY_TABLE[0]]
    return rng.choice(candidates)
