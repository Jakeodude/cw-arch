# worlds/content_warning/items.py

from itertools import groupby
from typing import Dict, List, Optional, Set, NamedTuple
from BaseClasses import Item, ItemClassification

from .names import item_names as iname


class ContentWarningItem(Item):
    game: str = "Content Warning"


item_base_id: int = 98765000


class CWItemData(NamedTuple):
    classification: ItemClassification
    quantity_in_item_pool: int
    item_id_offset: Optional[int]
    item_group: str = ""


# ==================== ITEM TABLE ====================
# quantity_in_item_pool sets the *base* count placed in the pool.
# create_items() adds random filler to fill any remaining slots.
#
# Filler rewards are ONLY: money, meta coins, or traps (per design notes).
item_table: Dict[str, CWItemData] = {

    # ---- Progressive Camera (Progression) ----
    # 3 upgrades: 90→120→150→180 seconds of film
    # Stage distribution: early/mid/late (handled in create_items)
    iname.prog_camera: CWItemData(ItemClassification.progression, 3, 0, "Camera"),

    # ---- Progressive Oxygen (Progression) ----
    # 4 upgrades: 500→700→900→1100→1500 seconds
    # Stage distribution: early/early/mid/late (handled in create_items)
    iname.prog_oxygen: CWItemData(ItemClassification.progression, 4, 1, "Oxygen"),

    # ---- Diving Bell Upgrades (Useful — mid game) ----
    iname.diving_bell_o2:      CWItemData(ItemClassification.useful, 1, 2, "Diving Bell"),
    iname.diving_bell_charger: CWItemData(ItemClassification.useful, 1, 3, "Diving Bell"),

    # ---- Progressive Views (Progression — mid/late game) ----
    # 12 copies; each multiplies view income by 1.1×
    iname.prog_views: CWItemData(ItemClassification.progression, 12, 4, "Views"),

    # ---- Rescue / Safety Gear (Progression) ----
    iname.rescue_hook:   CWItemData(ItemClassification.progression, 1, 10, "Safety"),
    iname.shock_stick:   CWItemData(ItemClassification.progression, 1, 11, "Safety"),
    iname.defibrillator: CWItemData(ItemClassification.progression, 1, 12, "Safety"),

    # ---- Money — filler ----
    # Small = $200, Medium = $400, Large = $600
    iname.money_small:  CWItemData(ItemClassification.filler, 3, 20, "Money"),
    iname.money_medium: CWItemData(ItemClassification.filler, 3, 21, "Money"),
    iname.money_large:  CWItemData(ItemClassification.filler, 2, 22, "Money"),

    # ---- Meta Coins — filler ----
    # Small = 1,000, Medium = 2,000, Large = 3,000
    # Design target: ≥40,000 total across a world (≥10k early, ≥20k mid, ≥10k late).
    # Base counts below total ~42,000 meta coins.
    iname.meta_coins_small:  CWItemData(ItemClassification.filler,  5, 30, "Meta Coins"),
    iname.meta_coins_medium: CWItemData(ItemClassification.filler,  8, 31, "Meta Coins"),
    iname.meta_coins_large:  CWItemData(ItemClassification.filler,  7, 32, "Meta Coins"),

    # ---- Traps ----
    # Monster Spawn: spawns a random monster from the trap list (not on Sky Island).
    # Ragdoll: ragdolls the player for 5 seconds.
    iname.monster_spawn: CWItemData(ItemClassification.trap, 3, 40, "Traps"),
    iname.ragdoll_trap:  CWItemData(ItemClassification.trap, 2, 41, "Traps"),

    # ---- Victory Event (no ID — placed as event) ----
    iname.viral_sensation: CWItemData(ItemClassification.progression, 0, None, "Event"),
}

# ==================== COMPUTED LOOKUPS ====================
item_name_to_id: Dict[str, Optional[int]] = {}

for _name, _data in item_table.items():
    if _data.item_id_offset is not None:
        item_name_to_id[_name] = item_base_id + _data.item_id_offset
    else:
        item_name_to_id[_name] = None


def _get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group


filler_items: List[str] = [
    name for name, data in item_table.items()
    if data.classification == ItemClassification.filler
]

trap_items: List[str] = [
    name for name, data in item_table.items()
    if data.classification == ItemClassification.trap
]

event_items: List[str] = [
    name for name, data in item_table.items()
    if data.item_group == "Event"
]

item_name_groups: Dict[str, Set[str]] = {
    group: set(names)
    for group, names in groupby(
        sorted(item_table, key=_get_item_group), _get_item_group
    )
    if group != ""
}

# ==================== MONSTER SPAWN TRAP POOL ====================
# Monsters that can be spawned by the Monster Spawn Trap.
# These are never spawned while the player is on Sky Island.
MONSTER_SPAWN_POOL: List[str] = [
    "Arms",
    "Bomber",
    "Zombe",
    "Spawn 3 Zombe",
    "Whisk",
    "Eye Guy",
    "Worm",
    "Knifo",
    "Dog",
    "Button Robot",
]
