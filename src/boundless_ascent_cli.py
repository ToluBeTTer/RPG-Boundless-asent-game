from __future__ import annotations

from boundless_ascent.gameplay import GameRuntime
from boundless_ascent.items import Item, ItemType

SHOP_ITEMS = {
    "steel_blade": Item("steel_blade", "Steel Blade", ItemType.WEAPON, value=75, power=7),
    "leather_armor": Item("leather_armor", "Leather Armor", ItemType.ARMOR, value=60, defense=5),
    "minor_potion": Item("minor_potion", "Minor Potion", ItemType.CONSUMABLE, value=10, heal=35, stackable=True),
    "focus_tonic": Item("focus_tonic", "Focus Tonic", ItemType.CONSUMABLE, value=14, essence_restore=25, stackable=True),
}


HELP_TEXT = """Commands:
  help
  create <name>|<description>
  profile
  build
  atlas
  world
  map
  landmarks
  npcs
  quest-board
  accept <quest_id>
  travel <zone name>
  explore
  delve [index]
  treasure
  inventory
  equip <item_id>
  use <item_id>
  shop
  buy <item_id>
  quests
  save <path>
  load <path>
  party-create <party_id>
  party-join <party_id>
  say <message>
  chat
  quit
"""


def execute_command(game: GameRuntime, raw: str) -> tuple[GameRuntime, str]:
    from boundless_ascent.persistence import load_character, save_character

    lower = raw.lower().strip()
    if lower == "help":
        return game, HELP_TEXT
    if lower.startswith("create "):
        body = raw[7:]
        if "|" not in body:
            return game, "Usage: create <name>|<description>"
        name, desc = [x.strip() for x in body.split("|", 1)]
        new_game = GameRuntime.from_description(name=name, description=desc, seed=game.seed)
        return new_game, f"Created AI build for {name}.\n{new_game.build_sheet()}"
    if lower == "profile":
        return game, game.profile()
    if lower == "build":
        return game, game.build_sheet()
    if lower == "atlas":
        return game, game.atlas()
    if lower == "world":
        return game, "Biomes: " + ", ".join(b.name for b in game.world.biomes)
    if lower == "map":
        return game, game.zone_map()
    if lower == "landmarks":
        return game, game.list_landmarks()
    if lower == "npcs":
        return game, game.list_npcs()
    if lower == "quest-board":
        return game, game.post_local_quests()
    if lower.startswith("accept "):
        return game, game.accept_quest(lower.split(maxsplit=1)[1])
    if lower.startswith("travel "):
        zone = raw[7:]
        return game, game.travel(zone)
    if lower == "explore":
        return game, game.explore()
    if lower.startswith("delve"):
        parts = lower.split()
        idx = 1 if len(parts) == 1 else max(1, int(parts[1]))
        return game, game.delve(idx)
    if lower == "treasure":
        return game, game.treasure_hunt()
    if lower == "inventory":
        rows = game.inventory.list_items()
        eq = f"Weapon={game.inventory.equipped_weapon} Armor={game.inventory.equipped_armor} Gold={game.inventory.gold}"
        return game, eq + "\n" + ("\n".join(rows) if rows else "Inventory empty.")
    if lower.startswith("equip "):
        return game, game.equip_item(lower.split(maxsplit=1)[1])
    if lower.startswith("use "):
        return game, game.use_item(lower.split(maxsplit=1)[1])
    if lower == "shop":
        return game, "\n".join(
            f"{item.item_id}: {item.name} ({item.item_type.value}) price={item.value}" for item in SHOP_ITEMS.values()
        )
    if lower.startswith("buy "):
        item_id = lower.split(maxsplit=1)[1]
        item = SHOP_ITEMS.get(item_id)
        if not item:
            return game, "No such shop item."
        return game, game.buy(item)
    if lower == "quests":
        return game, game.quest_status()
    if lower.startswith("save "):
        path = raw.split(maxsplit=1)[1]
        save_character(game.player, path)
        return game, f"Saved character to {path}"
    if lower.startswith("load "):
        path = raw.split(maxsplit=1)[1]
        game.player = load_character(path)
        game.server.state.sessions["local-player"].character = game.player
        return game, f"Loaded character from {path}"
    if lower.startswith("party-create "):
        party_id = lower.split(maxsplit=1)[1]
        game.server.create_party("local-player", party_id)
        return game, f"Created party {party_id}"
    if lower.startswith("party-join "):
        party_id = lower.split(maxsplit=1)[1]
        return game, "Joined party" if game.server.join_party("local-player", party_id) else "Party not found"
    if lower.startswith("say "):
        msg = raw.split(maxsplit=1)[1]
        game.server.apply_command("local-player", "chat", {"text": msg})
        return game, "Message sent."
    if lower == "chat":
        if not game.server.state.chat_log:
            return game, "Chat is empty."
        return game, "\n".join(f"[{m.tick}] {m.player_id}: {m.text}" for m in game.server.state.chat_log[-10:])
    if lower == "quit":
        return game, "quit"
    return game, "Unknown command. Type 'help'."


def main() -> None:
    game = GameRuntime()
    print("Boundless Ascent RPG Prototype (Open-World CLI)")
    print("Type 'help' for commands.")

    while True:
        try:
            raw = input("> ")
        except EOFError:
            break

        game, result = execute_command(game, raw)
        if result == "quit":
            print("Goodbye.")
            break
        print(result)
        game.server.tick()


if __name__ == "__main__":
    main()
