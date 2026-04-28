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

    # ---- Money — filler ----
    # Common: $50, $100, $200  |  Rare: $400
    # Base quantity is 0 — money is generated entirely via weighted random filler.
    iname.money_50:  CWItemData(ItemClassification.filler, 0, 19, "Money"),
    iname.money_100: CWItemData(ItemClassification.filler, 0, 20, "Money"),
    iname.money_200: CWItemData(ItemClassification.filler, 0, 21, "Money"),
    iname.money_300: CWItemData(ItemClassification.filler, 0, 22, "Money"),
    iname.money_400: CWItemData(ItemClassification.filler, 0, 23, "Money"),

    # ---- Meta Coins — filler ----
    # Four tiers; base quantities target ~40,000 MC total across a world.
    #
    # Early (~5,000):  4×500  + 3×1,000 = 5,000
    # Mid  (~15,000):  10×1,500          = 15,000
    # Late (~20,000):  10×2,000          = 20,000  (2,000 packages are rare)
    #
    # AP's early_items mechanism pushes 500/1,000 packages into sphere-1
    # locations to enforce the early distribution (see __init__.py).
    iname.meta_coins_500:  CWItemData(ItemClassification.filler,  4, 30, "Meta Coins"),
    iname.meta_coins_1000: CWItemData(ItemClassification.filler,  3, 31, "Meta Coins"),
    iname.meta_coins_1500: CWItemData(ItemClassification.filler, 10, 32, "Meta Coins"),
    iname.meta_coins_2000: CWItemData(ItemClassification.filler, 10, 33, "Meta Coins"),

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

# ---------------------------------------------------------------------------
# Weighted filler pools
# ---------------------------------------------------------------------------

# Money — common ($50/$100/$200) appear 3× as often as rare ($400).
# Using a flat population list so self.random.choice() gives natural weights.
MONEY_FILLER_POOL: List[str] = (
    [iname.money_50]  * 3 +
    [iname.money_100] * 3 +
    [iname.money_200] * 3 +
    [iname.money_400] * 1
)

# Meta Coins — additional random filler beyond the base pool quantities.
# 500/1,000 are common; 1,500 is mid-weight; 2,000 is rare.
META_COIN_FILLER_POOL: List[str] = (
    [iname.meta_coins_500]  * 4 +
    [iname.meta_coins_1000] * 4 +
    [iname.meta_coins_1500] * 2 +
    [iname.meta_coins_2000] * 1
)

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
