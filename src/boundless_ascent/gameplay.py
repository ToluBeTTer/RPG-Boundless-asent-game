from __future__ import annotations

from dataclasses import dataclass, field
from random import Random

from .ai_builder import AICharacterBuilder
from .character import Character, Race, Trait
from .combat import CombatEngine
from .content import WorldContent, generate_world_content
from .enemies import EnemyTemplate, roll_enemy
from .items import Inventory, STARTER_ITEMS, Item, ItemType
from .quests import Quest, QuestLog, QuestObjective, QuestReward, QuestStatus
from .server import GameServerState
from .world import World


@dataclass
class GameRuntime:
    seed: int = 42
    player: Character = field(default_factory=lambda: Character("Player", Race.HUMAN, Trait.PERCEPTIVE))
    world: World = field(default_factory=World.default_world)
    zone: str = "Verdant Frontier"
    inventory: Inventory = field(default_factory=Inventory)
    quest_log: QuestLog = field(default_factory=QuestLog)
    server: GameServerState = field(default_factory=GameServerState)
    generated_abilities: list[str] = field(default_factory=list)
    generated_passives: list[str] = field(default_factory=list)
    skill_tree: dict[str, list[str]] = field(default_factory=dict)
    content: WorldContent | None = None
    _rng: Random = field(init=False)

    def __post_init__(self) -> None:
        self._rng = Random(self.seed)
        self.server.connect_player("local-player", self.player)
        self.content = generate_world_content([b.name for b in self.world.biomes], seed=self.seed)
        self._grant_starter_pack()

    @classmethod
    def from_description(cls, name: str, description: str, seed: int = 42) -> "GameRuntime":
        generated = AICharacterBuilder.from_description(name, description)
        game = cls(seed=seed, player=generated.character)
        game.generated_abilities = generated.abilities
        game.generated_passives = generated.passives
        game.skill_tree = generated.skill_tree
        return game

    def _grant_starter_pack(self) -> None:
        for item in STARTER_ITEMS:
            qty = 3 if item.stackable else 1
            self.inventory.add_item(item, qty)
        self.inventory.equip("wood_blade")
        self.inventory.equip("cloth_wrap")
        self.quest_log.add_quest(
            Quest(
                quest_id="hunt_slimes",
                title="First Contract",
                objectives=[QuestObjective("kill_slime", 3)],
                reward=QuestReward(xp=140, stat_boost=1),
            )
        )

    def travel(self, zone: str) -> str:
        known = {b.name for b in self.world.biomes}
        if zone not in known:
            return f"Unknown zone: {zone}"
        self.zone = zone
        self.server.state.sessions["local-player"].zone = zone
        return f"Travelled to {zone}."

    def zone_map(self) -> str:
        return self.world.generate_zone_map(self.zone, seed=self.seed)

    def atlas(self) -> str:
        assert self.content is not None
        lines: list[str] = []
        for zone, region in self.content.regions.items():
            lines.append(f"[{zone}] landmarks={len(region.landmarks)} npcs={len(region.npcs)} dungeons={len(region.dungeons)}")
        return "\n".join(lines)

    def list_landmarks(self) -> str:
        assert self.content is not None
        region = self.content.region(self.zone)
        return "\n".join(f"- {l.kind}: {l.name} ({l.description})" for l in region.landmarks)

    def list_npcs(self) -> str:
        assert self.content is not None
        region = self.content.region(self.zone)
        return "\n".join(f"- {n.name} [{n.role}] quest={n.quest_id}" for n in region.npcs)

    def post_local_quests(self) -> str:
        assert self.content is not None
        region = self.content.region(self.zone)
        posted: list[str] = []
        for npc in region.npcs:
            quest_id = npc.quest_id or f"quest_{npc.name.replace(' ', '_').lower()}"
            if quest_id in self.quest_log.quests:
                continue
            quest = Quest(
                quest_id=quest_id,
                title=f"Task from {npc.name}",
                objectives=[QuestObjective(f"kill_{self.zone.lower().split()[0]}", 2)],
                reward=QuestReward(xp=90, stat_boost=1),
            )
            self.quest_log.add_quest(quest, activate=False)
            posted.append(quest.title)
        return "Posted quests:\n" + ("\n".join(posted) if posted else "No new quests")

    def accept_quest(self, quest_id: str) -> str:
        quest = self.quest_log.quests.get(quest_id)
        if not quest:
            return "Quest not found."
        quest.status = QuestStatus.ACTIVE
        return f"Accepted quest: {quest.title}"

    def delve(self, index: int = 1) -> str:
        assert self.content is not None
        region = self.content.region(self.zone)
        if not region.dungeons:
            return "No dungeons in this zone."
        dungeon = region.dungeons[max(0, min(index - 1, len(region.dungeons) - 1))]

        total_xp = 0
        total_gold = 0
        for _ in range(dungeon.difficulty + 1):
            enemy = roll_enemy(self.zone, self._rng)
            result = self.battle_enemy(enemy)
            if "defeated by" in result.lower():
                return f"Failed dungeon run at {dungeon.name}."
            total_xp += enemy.xp_reward
            total_gold += enemy.gold_reward

        reward_item = Item(
            item_id=f"relic_{dungeon.name.lower().replace(' ', '_')}",
            name=f"Relic of {dungeon.name}",
            item_type=ItemType.QUEST,
            value=120,
        )
        self.inventory.add_item(reward_item)
        return (
            f"Cleared {dungeon.name} (difficulty {dungeon.difficulty}) | gained approx {total_xp} xp, {total_gold}g "
            f"and found {reward_item.name} ({dungeon.reward_hint})."
        )

    def treasure_hunt(self) -> str:
        found_gold = self._rng.randint(10, 60)
        self.inventory.gold += found_gold
        if self._rng.random() < 0.4:
            item = Item("mystic_cache", "Mystic Cache", ItemType.CONSUMABLE, value=30, essence_restore=20)
            self.inventory.add_item(item)
            return f"Found treasure chest: +{found_gold}g and {item.name}."
        return f"Found treasure chest: +{found_gold}g."

    def explore(self) -> str:
        enemy = roll_enemy(self.zone, self._rng)
        return self.battle_enemy(enemy)

    def battle_enemy(self, enemy_template: EnemyTemplate) -> str:
        enemy = Character(
            name=enemy_template.name,
            race=Race.VOID_MARKED,
            trait=Trait.RELENTLESS,
            hp=enemy_template.hp,
        )
        enemy.stats.strength = enemy_template.attack
        enemy.stats.endurance = enemy_template.defense + 8

        rounds = 0
        while self.player.hp > 0 and enemy.hp > 0 and rounds < 30:
            rounds += 1
            try:
                CombatEngine.basic_attack(self.player, enemy)
            except ValueError:
                self.player.stamina = min(100, self.player.stamina + 8)

            if enemy.hp <= 0:
                break

            try:
                CombatEngine.basic_attack(enemy, self.player)
            except ValueError:
                enemy.stamina = min(100, enemy.stamina + 8)

        if self.player.hp <= 0:
            self.player.hp = 30
            return f"You were defeated by {enemy.name}. You recover at camp with 30 HP."

        self.player.gain_xp(enemy_template.xp_reward)
        self.inventory.gold += enemy_template.gold_reward

        for drop in enemy_template.drops:
            self.inventory.add_item(drop, 1)

        event_key = "kill_slime" if enemy_template.enemy_id == "slime" else f"kill_{enemy_template.enemy_id}"
        completed = self.quest_log.record_event(event_key, 1)
        self.quest_log.apply_rewards(self.player, completed)

        drops = ", ".join(d.name for d in enemy_template.drops)
        return (
            f"Defeated {enemy.name} in {rounds} rounds. +{enemy_template.xp_reward} XP, "
            f"+{enemy_template.gold_reward}g, drops: {drops}."
        )

    def use_item(self, item_id: str) -> str:
        item = self.inventory.use(item_id)
        if not item:
            return "Item cannot be used."
        if item.heal:
            self.player.hp = min(200, self.player.hp + item.heal)
        if item.essence_restore:
            self.player.essence_pool = min(200, self.player.essence_pool + item.essence_restore)
        return f"Used {item.name}."

    def equip_item(self, item_id: str) -> str:
        if self.inventory.equip(item_id):
            return f"Equipped {self.inventory.catalog[item_id].name}."
        return "Unable to equip that item."

    def buy(self, item: Item) -> str:
        if self.inventory.gold < item.value:
            return "Not enough gold."
        self.inventory.gold -= item.value
        self.inventory.add_item(item, 1)
        return f"Purchased {item.name}."

    def profile(self) -> str:
        return (
            f"{self.player.name} | lvl {self.player.level} | hp {self.player.hp} | "
            f"stamina {self.player.stamina} | essence {self.player.essence_pool} | gold {self.inventory.gold} | zone {self.zone}"
        )

    def build_sheet(self) -> str:
        return (
            f"Abilities: {', '.join(self.generated_abilities) if self.generated_abilities else 'None'}\n"
            f"Passives: {', '.join(self.generated_passives) if self.generated_passives else 'None'}\n"
            f"Skill Tree: {self.skill_tree if self.skill_tree else '{}'}"
        )

    def quest_status(self) -> str:
        rows = []
        for quest in self.quest_log.quests.values():
            progress = ", ".join(f"{o.key}:{o.progress}/{o.target}" for o in quest.objectives)
            rows.append(f"{quest.quest_id}: {quest.title} [{quest.status.value}] {progress}")
        return "\n".join(rows) if rows else "No quests."
