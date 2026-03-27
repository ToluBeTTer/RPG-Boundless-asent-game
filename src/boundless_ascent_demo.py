from pathlib import Path

from boundless_ascent.abilities import AbilityBlueprint, AbilityBuilder, EnergyLayer, MoveType
from boundless_ascent.ai import EncounterEngine
from boundless_ascent.character import Character, Race, Trait
from boundless_ascent.combat import CombatEngine
from boundless_ascent.crafting import CraftingEngine, Material
from boundless_ascent.persistence import load_character, save_character
from boundless_ascent.quests import Quest, QuestLog, QuestObjective, QuestReward
from boundless_ascent.server import GameServerState
from boundless_ascent.world import World


def main() -> None:
    world = World.default_world()
    print(f"World: {world.name} | biomes={len(world.biomes)}")

    hero = Character(name="Astra", race=Race.HUMAN, trait=Trait.RESONANT_SOUL)
    boss = Character(name="Marsh Warden", race=Race.VOID_MARKED, trait=Trait.RELENTLESS, hp=180)

    hero.gain_xp(350)
    hero.train_vital(3)
    hero.train_soul(4)

    shadow_ore = Material("Void Ore", weight=7, durability=25, resonance="shadow")
    storm_fang = Material("Storm Fang", weight=4, durability=14, resonance="lightning")
    blade = CraftingEngine.craft_weapon("Dusktooth", [shadow_ore, storm_fang])
    print(f"Crafted weapon: {blade.name} atk={blade.attack} res={sorted(blade.resonances)}")

    blueprint = AbilityBlueprint(
        name="Void Flash",
        move_type=MoveType.DASH,
        energy_layer=EnergyLayer.SOUL,
        element="shadow",
        range_score=2,
        size_score=2,
        charge_score=2,
    )
    ability = AbilityBuilder.build(hero, blueprint)

    result = CombatEngine.use_ability(hero, boss, ability)
    print(
        f"{result.attacker} used {result.used_ability} on {result.defender}: "
        f"damage={result.damage}, hp_after={result.defender_hp_after}"
    )

    # Quest / event pipeline
    quest_log = QuestLog()
    quest_log.add_quest(
        Quest(
            quest_id="q_slime_01",
            title="First Hunt",
            objectives=[QuestObjective("slime_defeated", target=3)],
            reward=QuestReward(xp=120, stat_boost=1),
        )
    )
    done = quest_log.record_event("slime_defeated", value=3)
    quest_log.apply_rewards(hero, done)
    print(f"Completed quests: {len(done)} | hero level={hero.level}")

    # Persistence save/load
    save_path = Path("/tmp/boundless_ascent_demo_character.json")
    save_character(hero, save_path)
    loaded = load_character(save_path)
    print(f"Loaded character: {loaded.name} lvl={loaded.level} soul={loaded.power_layers.soul_aether}")

    # Encounter AI
    encounter = EncounterEngine()
    duel_enemy = Character(name="Bog Wolf", race=Race.VOID_MARKED, trait=Trait.RELENTLESS, hp=70)
    outcome = encounter.run_duel(hero, duel_enemy)
    print(f"Encounter winner: {outcome.winner} in {outcome.rounds} rounds")

    # Network-ready server state model
    server = GameServerState()
    server.connect_player("player-1", hero)
    server.apply_command("player-1", "move", {"dx": 2, "dy": -1})
    server.apply_command("player-1", "meditate")
    server.tick()
    pos = server.state.sessions["player-1"]
    print(f"Server tick={server.state.tick} pos=({pos.x},{pos.y})")


if __name__ == "__main__":
    main()
