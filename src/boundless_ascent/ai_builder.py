from __future__ import annotations

from dataclasses import dataclass

from .character import Character, Race, Trait


@dataclass
class GeneratedBuild:
    character: Character
    abilities: list[str]
    passives: list[str]
    skill_tree: dict[str, list[str]]
    summary: str


class AICharacterBuilder:
    """Rule-based stand-in for AI interpretation of free-text character concepts."""

    KEYWORDS = {
        "sword": ("strength", "Blade Focus", "Combo Edge", "Sword Saint"),
        "assassin": ("agility", "Shadow Step", "Critical Flow", "Night Oath"),
        "mage": ("essence", "Arc Burst", "Mana Weave", "Astral Core"),
        "tank": ("endurance", "Iron Guard", "Fortress Body", "Unbreakable"),
        "healer": ("control", "Renew Pulse", "Life Weave", "Saint Circuit"),
        "summon": ("resonance", "Spirit Call", "Bond Mastery", "Legion Link"),
        "dragon": ("essence", "Drake Flame", "Scale Aura", "Dragonheart"),
        "lightning": ("agility", "Volt Dash", "Storm Reflex", "Tempest Crown"),
        "shadow": ("control", "Umbral Bind", "Dark Precision", "Abyss Sigil"),
    }

    @classmethod
    def from_description(cls, name: str, description: str) -> GeneratedBuild:
        text = description.lower()
        race = cls._infer_race(text)
        trait = cls._infer_trait(text)
        character = Character(name=name, race=race, trait=trait)

        stat_bias: dict[str, int] = {
            "strength": 0,
            "agility": 0,
            "essence": 0,
            "endurance": 0,
            "control": 0,
            "resonance": 0,
        }
        abilities: list[str] = []
        passives: list[str] = []
        capstones: list[str] = []

        for keyword, (stat, ability, passive, capstone) in cls.KEYWORDS.items():
            if keyword in text:
                stat_bias[stat] += 4
                abilities.append(ability)
                passives.append(passive)
                capstones.append(capstone)

        if not abilities:
            abilities = ["Aether Bolt"]
            passives = ["Adaptive Instinct"]
            capstones = ["Boundless Seed"]
            stat_bias["essence"] += 2
            stat_bias["agility"] += 2

        cls._apply_stats(character, stat_bias)

        skill_tree = {
            "Novice": abilities[:2],
            "Adept": passives[:2],
            "Ascendant": capstones[:2],
        }
        summary = (
            f"AI generated {race.value} {trait.value} build with focus on "
            f"{', '.join([k for k, v in stat_bias.items() if v > 0])}."
        )

        return GeneratedBuild(
            character=character,
            abilities=abilities,
            passives=passives,
            skill_tree=skill_tree,
            summary=summary,
        )

    @staticmethod
    def _apply_stats(character: Character, stat_bias: dict[str, int]) -> None:
        character.stats.strength += stat_bias["strength"]
        character.stats.agility += stat_bias["agility"]
        character.stats.essence += stat_bias["essence"]
        character.stats.endurance += stat_bias["endurance"]
        character.stats.control += stat_bias["control"]
        character.stats.resonance += stat_bias["resonance"]

    @staticmethod
    def _infer_race(text: str) -> Race:
        if "celestial" in text or "angel" in text:
            return Race.CELESTIAL_BORN
        if "spirit" in text or "summon" in text:
            return Race.SPIRIT_TOUCHED
        if "void" in text or "shadow" in text:
            return Race.VOID_MARKED
        return Race.HUMAN

    @staticmethod
    def _infer_trait(text: str) -> Trait:
        if "memory" in text or "tactician" in text:
            return Trait.IRON_MEMORY
        if "percept" in text or "detect" in text:
            return Trait.PERCEPTIVE
        if "reson" in text or "element" in text:
            return Trait.RESONANT_SOUL
        return Trait.RELENTLESS
