from boundless_ascent.gameplay import GameRuntime


def main() -> None:
    game = GameRuntime.from_description(
        name="Astra",
        description="shadow lightning assassin swordsman with spirit resonance",
        seed=7,
    )
    print("== Boundless Ascent Demo ==")
    print(game.profile())
    print(game.build_sheet())
    print("-- Atlas --")
    print(game.atlas())
    print("-- Zone Map --")
    print(game.zone_map())
    print("-- Landmarks --")
    print(game.list_landmarks())
    print("-- NPCs --")
    print(game.list_npcs())
    print(game.post_local_quests())
    print(game.explore())
    print(game.delve(1))
    print(game.treasure_hunt())
    print(game.quest_status())


if __name__ == "__main__":
    main()
