from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .character import Character, PowerLayers, Race, Stats, Trait


def character_to_dict(character: Character) -> dict:
    data = asdict(character)
    data["race"] = character.race.value
    data["trait"] = character.trait.value
    return data


def character_from_dict(data: dict) -> Character:
    stats_data = data.get("stats", {})
    layers_data = data.get("power_layers", {})
    return Character(
        name=data["name"],
        race=Race(data["race"]),
        trait=Trait(data["trait"]),
        level=data.get("level", 1),
        xp=data.get("xp", 0),
        hp=data.get("hp", 100),
        stamina=data.get("stamina", 100),
        essence_pool=data.get("essence_pool", 100),
        stats=Stats(**stats_data),
        power_layers=PowerLayers(**layers_data),
    )


def save_character(character: Character, path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(character_to_dict(character), indent=2), encoding="utf-8")


def load_character(path: str | Path) -> Character:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    return character_from_dict(data)
