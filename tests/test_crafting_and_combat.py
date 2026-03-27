import unittest

from boundless_ascent.abilities import AbilityBlueprint, AbilityBuilder, EnergyLayer, MoveType
from boundless_ascent.character import Character, Race, Trait
from boundless_ascent.combat import CombatEngine
from boundless_ascent.crafting import CraftingEngine, Material


class CraftingAndCombatTests(unittest.TestCase):
    def test_weapon_fusion_combines_resonances(self):
        w1 = CraftingEngine.craft_weapon(
            "W1",
            [Material("Void Ore", 7, 20, "shadow")],
        )
        w2 = CraftingEngine.craft_weapon(
            "W2",
            [Material("Storm Fang", 4, 12, "lightning")],
        )
        fused = CraftingEngine.fuse_weapons("Fusion", w1, w2)
        self.assertEqual(fused.resonances, {"shadow", "lightning"})

    def test_combat_ability_deals_damage(self):
        a = Character(name="A", race=Race.HUMAN, trait=Trait.PERCEPTIVE)
        b = Character(name="B", race=Race.VOID_MARKED, trait=Trait.RELENTLESS)
        blueprint = AbilityBlueprint(
            name="Arc Bolt",
            move_type=MoveType.PROJECTILE,
            energy_layer=EnergyLayer.SOUL,
            element="arc",
            range_score=2,
            size_score=2,
            charge_score=2,
        )
        ability = AbilityBuilder.build(a, blueprint)
        before = b.hp
        result = CombatEngine.use_ability(a, b, ability)
        self.assertLess(result.defender_hp_after, before)


if __name__ == "__main__":
    unittest.main()
