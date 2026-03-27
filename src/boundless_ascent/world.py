from __future__ import annotations

from dataclasses import dataclass, field


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
