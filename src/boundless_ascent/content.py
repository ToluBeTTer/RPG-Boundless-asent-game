from __future__ import annotations

from dataclasses import dataclass, field
from random import Random


@dataclass
class Landmark:
    name: str
    kind: str
    zone: str
    description: str


@dataclass
class NPC:
    name: str
    role: str
    zone: str
    quest_id: str | None = None


@dataclass
class Dungeon:
    name: str
    zone: str
    difficulty: int
    reward_hint: str


@dataclass
class RegionContent:
    zone: str
    landmarks: list[Landmark] = field(default_factory=list)
    npcs: list[NPC] = field(default_factory=list)
    dungeons: list[Dungeon] = field(default_factory=list)


@dataclass
class WorldContent:
    regions: dict[str, RegionContent]

    def region(self, zone: str) -> RegionContent:
        return self.regions[zone]


def generate_world_content(zones: list[str], seed: int = 42) -> WorldContent:
    rng = Random(seed)

    village_names = ["Aetherford", "Runehaven", "Mistgrove", "Sunspire", "Stormrest"]
    mine_names = ["Ironvein Mine", "Moonrock Pit", "Deep Echo Mine", "Crystalfall Mine"]
    tower_names = ["Obsidian Wizard Tower", "Celestial Observatory", "Umbral Spire", "Stormcall Tower"]
    dungeon_names = ["Abyss Vault", "Shattered Catacombs", "Eclipse Labyrinth", "Titan Reliquary"]
    npc_roles = ["Blacksmith", "Guildmaster", "Alchemist", "Ranger", "Archivist", "Scout"]

    regions: dict[str, RegionContent] = {}

    for zone in zones:
        landmarks = [
            Landmark(rng.choice(village_names), "Village", zone, "A safe hub with vendors and quest board."),
            Landmark(rng.choice(mine_names), "Mine", zone, "Resource extraction site with hostile tunnels."),
            Landmark(rng.choice(tower_names), "Wizard Tower", zone, "Arcane trial site with puzzles and relics."),
            Landmark(f"{zone} Trial Chamber", "Trial Chamber", zone, "Timed combat trial with elite rewards."),
            Landmark(f"{zone} Treasure Site", "Treasure Spot", zone, "Hidden chest area guarded by monsters."),
        ]

        npcs = [
            NPC(name=f"{rng.choice(['Eli', 'Mira', 'Kael', 'Rin', 'Sora'])} the {role}", role=role, zone=zone)
            for role in rng.sample(npc_roles, k=3)
        ]

        quest_base = zone.lower().replace(" ", "_")
        for i, npc in enumerate(npcs, start=1):
            npc.quest_id = f"quest_{quest_base}_{i}"

        dungeons = [
            Dungeon(
                name=f"{rng.choice(dungeon_names)} ({zone})",
                zone=zone,
                difficulty=max(1, i + 1),
                reward_hint=rng.choice(["relic gear", "rare core", "skill scroll", "ascension shard"]),
            )
            for i in range(2)
        ]

        regions[zone] = RegionContent(zone=zone, landmarks=landmarks, npcs=npcs, dungeons=dungeons)

    return WorldContent(regions=regions)
