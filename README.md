# Boundless Ascent Prototype

This repository contains an **initial game backend prototype** for Boundless Ascent, focused on core simulation systems.

## What's implemented
- Character model with races, traits, layered power progression, XP leveling, and origin awakening.
- Ability builder with point-budget validation and energy layer scaling.
- Crafting and fusion systems for weapons and armor.
- Core action-combat resolution (basic attacks + abilities).
- Seeded world/biome model.
- Persistence layer for save/load character snapshots.
- Enemy AI and encounter loop for autonomous duels.
- Quest/event pipeline with objective tracking and reward application.
- Network-ready server state model with sessions, commands, and ticks.
- Unit tests for progression, ability constraints, crafting fusion, combat, persistence, AI, quests, and server state.

## Run tests
```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py' -v
```

## Quick demo
```bash
PYTHONPATH=src python -m boundless_ascent_demo
```
