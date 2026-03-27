from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ItemType(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    MATERIAL = "material"
    QUEST = "quest"


@dataclass
class Item:
    item_id: str
    name: str
    item_type: ItemType
    value: int = 0
    power: int = 0
    defense: int = 0
    heal: int = 0
    essence_restore: int = 0
    stackable: bool = False


@dataclass
class Inventory:
    gold: int = 100
    items: dict[str, int] = field(default_factory=dict)
    catalog: dict[str, Item] = field(default_factory=dict)
    equipped_weapon: str | None = None
    equipped_armor: str | None = None

    def add_item(self, item: Item, qty: int = 1) -> None:
        self.catalog[item.item_id] = item
        self.items[item.item_id] = self.items.get(item.item_id, 0) + qty

    def remove_item(self, item_id: str, qty: int = 1) -> bool:
        owned = self.items.get(item_id, 0)
        if owned < qty:
            return False
        self.items[item_id] = owned - qty
        if self.items[item_id] == 0:
            del self.items[item_id]
        return True

    def list_items(self) -> list[str]:
        rows: list[str] = []
        for item_id, qty in sorted(self.items.items()):
            item = self.catalog[item_id]
            rows.append(f"{item.name} x{qty}")
        return rows

    def equip(self, item_id: str) -> bool:
        if item_id not in self.items:
            return False
        item = self.catalog[item_id]
        if item.item_type == ItemType.WEAPON:
            self.equipped_weapon = item_id
            return True
        if item.item_type == ItemType.ARMOR:
            self.equipped_armor = item_id
            return True
        return False

    def use(self, item_id: str) -> Item | None:
        if item_id not in self.items:
            return None
        item = self.catalog[item_id]
        if item.item_type != ItemType.CONSUMABLE:
            return None
        if not self.remove_item(item_id, 1):
            return None
        return item

    @property
    def weapon_power(self) -> int:
        if self.equipped_weapon and self.equipped_weapon in self.catalog:
            return self.catalog[self.equipped_weapon].power
        return 0

    @property
    def armor_defense(self) -> int:
        if self.equipped_armor and self.equipped_armor in self.catalog:
            return self.catalog[self.equipped_armor].defense
        return 0


STARTER_ITEMS: list[Item] = [
    Item("wood_blade", "Wood Blade", ItemType.WEAPON, value=20, power=3),
    Item("cloth_wrap", "Cloth Wrap", ItemType.ARMOR, value=15, defense=2),
    Item("minor_potion", "Minor Potion", ItemType.CONSUMABLE, value=10, heal=35, stackable=True),
    Item("focus_tonic", "Focus Tonic", ItemType.CONSUMABLE, value=14, essence_restore=25, stackable=True),
]
