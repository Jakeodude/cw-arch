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
# quantity_in_item_pool sets the *base* count; create_items() adds filler to fill remaining slots.
item_table: Dict[str, CWItemData] = {

    # ---- Camera Equipment (Progression) ----
    iname.camera_upgrade:  CWItemData(ItemClassification.progression, 1,  0, "Equipment"),
    iname.advanced_camera: CWItemData(ItemClassification.progression, 1,  1, "Equipment"),
    iname.parabolic_mic:   CWItemData(ItemClassification.progression, 1,  2, "Equipment"),
    iname.rescue_hook:     CWItemData(ItemClassification.progression, 1,  3, "Equipment"),
    iname.shock_stick:     CWItemData(ItemClassification.progression, 1,  4, "Equipment"),
    iname.goo_ball_pack:   CWItemData(ItemClassification.useful,      2,  5, "Equipment"),
    iname.defibrillator:   CWItemData(ItemClassification.progression, 1,  6, "Equipment"),

    # ---- Health & Oxygen (Progression / Useful) ----
    iname.increased_health:    CWItemData(ItemClassification.progression, 2, 10, "Health"),
    iname.health_upgrade:      CWItemData(ItemClassification.useful,      2, 11, "Health"),
    iname.increased_oxygen:    CWItemData(ItemClassification.progression, 2, 12, "Oxygen"),
    iname.oxygen_tank_upgrade: CWItemData(ItemClassification.useful,      2, 13, "Oxygen"),
    iname.extra_oxygen:        CWItemData(ItemClassification.filler,      2, 14, "Oxygen"),

    # ---- Money (Useful / Filler) ----
    iname.money_boost:     CWItemData(ItemClassification.useful,  3, 20, "Money"),
    iname.big_money_boost: CWItemData(ItemClassification.useful,  2, 21, "Money"),
    iname.extra_cash:      CWItemData(ItemClassification.filler,  3, 22, "Money"),
    iname.cash_500:        CWItemData(ItemClassification.filler,  2, 23, "Money"),
    iname.cash_2000:       CWItemData(ItemClassification.useful,  2, 24, "Money"),

    # ---- Meta Coins (Filler / Useful) ----
    iname.meta_coin:          CWItemData(ItemClassification.filler,  3, 30, "Meta Coins"),
    iname.meta_coin_pack:     CWItemData(ItemClassification.useful,  2, 31, "Meta Coins"),
    iname.big_meta_coin_pack: CWItemData(ItemClassification.useful,  1, 32, "Meta Coins"),

    # ---- View Boosts (Progression — gates view milestone checks) ----
    iname.view_boost:     CWItemData(ItemClassification.progression, 4, 40, "Views"),
    iname.big_view_boost: CWItemData(ItemClassification.progression, 2, 41, "Views"),
    iname.viral_moment:   CWItemData(ItemClassification.useful,      2, 42, "Views"),

    # ---- Filler ----
    iname.nothing:           CWItemData(ItemClassification.filler, 2, 50, "Filler"),
    iname.extra_views:       CWItemData(ItemClassification.filler, 2, 51, "Filler"),
    iname.small_cash:        CWItemData(ItemClassification.filler, 2, 52, "Filler"),
    iname.minor_health_pack: CWItemData(ItemClassification.filler, 2, 53, "Filler"),
    iname.minor_oxygen:      CWItemData(ItemClassification.filler, 2, 54, "Filler"),
    iname.monster_repellent: CWItemData(ItemClassification.filler, 2, 55, "Filler"),

    # ---- Traps ----
    iname.camera_malfunction: CWItemData(ItemClassification.trap, 2, 60, "Traps"),
    iname.monster_swarm:      CWItemData(ItemClassification.trap, 1, 61, "Traps"),
    iname.oxygen_leak:        CWItemData(ItemClassification.trap, 1, 62, "Traps"),
    iname.low_battery:        CWItemData(ItemClassification.trap, 1, 63, "Traps"),

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
