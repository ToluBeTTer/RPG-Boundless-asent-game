"""Boundless Ascent core prototype package."""

from .abilities import AbilityBlueprint, AbilityBuilder
from .ai import EncounterEngine, EnemyBehavior, EnemyController
from .ai_builder import AICharacterBuilder, GeneratedBuild
from .character import Character, Race, Trait
from .combat import CombatEngine, CombatResult
from .crafting import Armor, CraftingEngine, Material, Weapon
from .content import Dungeon, Landmark, NPC, RegionContent, WorldContent
from .enemies import EnemyTemplate
from .gameplay import GameRuntime
from .items import Inventory, Item, ItemType
from .persistence import load_character, save_character
from .quests import Quest, QuestLog, QuestObjective, QuestReward
from .server import ChatMessage, GameServerState, PlayerSession, WorldState
from .world import Biome, World

__all__ = [
    "Character",
    "Race",
    "Trait",
    "World",
    "Biome",
    "CombatEngine",
    "CombatResult",
    "AbilityBlueprint",
    "AbilityBuilder",
    "Material",
    "Weapon",
    "Armor",
    "CraftingEngine",
    "Landmark",
    "NPC",
    "Dungeon",
    "RegionContent",
    "WorldContent",
    "EnemyTemplate",
    "GameRuntime",
    "AICharacterBuilder",
    "GeneratedBuild",
    "Item",
    "ItemType",
    "Inventory",
    "save_character",
    "load_character",
    "EnemyBehavior",
    "EnemyController",
    "EncounterEngine",
    "Quest",
    "QuestLog",
    "QuestObjective",
    "QuestReward",
    "GameServerState",
    "PlayerSession",
    "WorldState",
    "ChatMessage",
]
