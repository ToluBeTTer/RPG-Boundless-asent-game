from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Race(str, Enum):
    HUMAN = "Human"
    CELESTIAL_BORN = "Celestial-Born"
    SPIRIT_TOUCHED = "Spirit-Touched"
    VOID_MARKED = "Void-Marked"


class Trait(str, Enum):
    RELENTLESS = "Relentless"
    PERCEPTIVE = "Perceptive"
    IRON_MEMORY = "Iron Memory"
    RESONANT_SOUL = "Resonant Soul"


@dataclass
class Stats:
    strength: int = 10
    agility: int = 10
    endurance: int = 10
    essence: int = 10
    control: int = 10
    resonance: int = 10
    origin: int = 0


@dataclass
class PowerLayers:
    vital_aether: int = 1
    soul_aether: int = 1
    origin_flame: int = 0


@dataclass
class Character:
    name: str
    race: Race
    trait: Trait
    level: int = 1
    xp: int = 0
    hp: int = 100
    stamina: int = 100
    essence_pool: int = 100
    stats: Stats = field(default_factory=Stats)
    power_layers: PowerLayers = field(default_factory=PowerLayers)

    def gain_xp(self, amount: int) -> bool:
        self.xp += amount
        levelled = False
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            self._on_level_up()
            levelled = True
        return levelled

    @property
    def xp_to_next_level(self) -> int:
        return 100 + (self.level - 1) * 25

    @property
    def attack_power(self) -> int:
        return self.stats.strength * 2 + self.power_layers.vital_aether

    @property
    def defense(self) -> int:
        return self.stats.endurance * 2 + self.power_layers.vital_aether

    def apply_damage(self, amount: int) -> int:
        mitigated = max(1, amount - self.defense // 4)
        self.hp = max(0, self.hp - mitigated)
        return mitigated

    def spend_stamina(self, amount: int) -> bool:
        if self.stamina < amount:
            return False
        self.stamina -= amount
        return True

    def spend_essence(self, amount: int) -> bool:
        if self.essence_pool < amount:
            return False
        self.essence_pool -= amount
        return True

    def train_vital(self, amount: int = 1) -> None:
        self.power_layers.vital_aether += amount

    def train_soul(self, amount: int = 1) -> None:
        self.power_layers.soul_aether += amount

    def awaken_origin(self) -> bool:
        if self.level < 10 or self.power_layers.vital_aether < 10 or self.power_layers.soul_aether < 10:
            return False
        if self.power_layers.origin_flame == 0:
            self.power_layers.origin_flame = 1
            self.stats.origin = 1
            return True
        self.power_layers.origin_flame += 1
        self.stats.origin += 1
        return True

    def _on_level_up(self) -> None:
        self.hp += 10
        self.stamina += 5
        self.essence_pool += 5
        self.stats.strength += 1
        self.stats.agility += 1
        self.stats.endurance += 1
        self.stats.essence += 1
        self.stats.control += 1
        self.stats.resonance += 1
