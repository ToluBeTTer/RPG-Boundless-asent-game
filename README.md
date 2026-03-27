# Boundless Ascent Prototype (Playable Open-World RPG)

This repository contains a **playable pixel-style open-world RPG prototype** with:
- AI-assisted character creation from free-text descriptions,
- generated abilities/passives/skill tree,
- biome maps with procedural landmarks (villages, mines, wizard towers, trial chambers, treasure spots),
- NPC listings and zone quest boards,
- dungeon delves + treasure hunts,
- combat, loot, quests, progression,
- inventory/equipment, shop economy,
- save/load persistence,
- party + chat server simulation (single-player first).

> Current scope: rich single-player RPG loop with MMO-like systems; not a full networked production MMORPG client.

## Play now
```bash
PYTHONPATH=src python -m boundless_ascent_cli
```

## Build your AI-generated character
In CLI:
```text
create Astra|shadow lightning assassin swordsman with spirit resonance
build
```

## Open-world commands
- `atlas` (zone summary)
- `world` (biome list)
- `map` (pixel map)
- `landmarks`
- `npcs`
- `quest-board`
- `accept <quest_id>`
- `travel <zone name>`
- `explore`
- `delve [index]`
- `treasure`

## RPG/system commands
- `profile`
- `inventory`
- `equip <item_id>`
- `use <item_id>`
- `shop`
- `buy <item_id>`
- `quests`
- `save <path>`
- `load <path>`
- `party-create <party_id>`
- `party-join <party_id>`
- `say <message>`
- `chat`
- `quit`

## Run demo
```bash
PYTHONPATH=src python -m boundless_ascent_demo
```

## Run tests
```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py' -v
```
