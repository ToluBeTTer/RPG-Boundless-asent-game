from __future__ import annotations

from dataclasses import dataclass, field
from random import Random


@dataclass(frozen=True)
class Biome:
    name: str
    danger_level: int
    resource_tags: tuple[str, ...]


@dataclass
class World:
    name: str = "Echoes of Ascension"
    biomes: list[Biome] = field(default_factory=list)

    def add_biome(self, biome: Biome) -> None:
        self.biomes.append(biome)

    def generate_zone_map(self, zone: str, width: int = 20, height: int = 10, seed: int = 1) -> str:
        rng = Random(hash((zone, seed)) & 0xFFFFFFFF)
        palette = self._palette_for_zone(zone)
        rows: list[str] = []
        for _ in range(height):
            row = "".join(rng.choice(palette) for _ in range(width))
            rows.append(row)
        return "\n".join(rows)

    @staticmethod
    def _palette_for_zone(zone: str) -> list[str]:
        z = zone.lower()
        if "verdant" in z:
            return list("..,,'" + "TT" + "~~")
        if "highland" in z:
            return list("^^..rr")
        if "cursed" in z:
            return list("..mmxx~~")
        if "volcanic" in z:
            return list("..##LL")
        if "rift" in z:
            return list(".. 00@@")
        return list("...,,,~~")

    @classmethod
    def default_world(cls) -> "World":
        world = cls()
        world.biomes.extend(
            [
                Biome("Verdant Frontier", danger_level=1, resource_tags=("wood", "water", "herb")),
                Biome("Highland Ruins", danger_level=3, resource_tags=("stone", "ancient", "ore")),
                Biome("Cursed Marshlands", danger_level=4, resource_tags=("toxin", "cursed", "fungal")),
                Biome("Volcanic Flame Territory", danger_level=5, resource_tags=("magma", "fire", "rare_ore")),
                Biome("Dimensional Rift Zone", danger_level=8, resource_tags=("void", "fracture", "relic")),
            ]
        )
        return world
