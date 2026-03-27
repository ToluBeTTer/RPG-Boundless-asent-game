import unittest

from boundless_ascent.abilities import AbilityBlueprint, AbilityBuilder, EnergyLayer, MoveType
from boundless_ascent.character import Character, Race, Trait


class AbilityBuilderTests(unittest.TestCase):
    def setUp(self):
        self.character = Character(name="A", race=Race.HUMAN, trait=Trait.RESONANT_SOUL)

    def test_build_ability_within_budget(self):
        blueprint = AbilityBlueprint(
            name="Pulse",
            move_type=MoveType.PROJECTILE,
            energy_layer=EnergyLayer.SOUL,
            element="arcane",
            range_score=2,
            size_score=2,
            charge_score=1,
        )
        ability = AbilityBuilder.build(self.character, blueprint)
        self.assertGreater(ability.power, 0)

    def test_reject_over_budget_blueprint(self):
        blueprint = AbilityBlueprint(
            name="TooBig",
            move_type=MoveType.DOMAIN,
            energy_layer=EnergyLayer.SOUL,
            element="void",
            range_score=10,
            size_score=10,
            charge_score=10,
        )
        with self.assertRaises(ValueError):
            AbilityBuilder.build(self.character, blueprint)


if __name__ == "__main__":
    unittest.main()
