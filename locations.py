# worlds/content_warning/locations.py

from typing import Dict, List, Optional, Set, Tuple, NamedTuple
from BaseClasses import Location

from .names import region_names as rname
from .names import location_names as lname


class ContentWarningLocation(Location):
    game: str = "Content Warning"


location_base_id: int = 98765000


class CWLocationData(NamedTuple):
    region: str
    location_id_offset: int
    location_group: Optional[str] = None
    # game_stage: "early", "mid", "late", "filler", or "difficult"
    # "filler"    — always receives only a filler item (never progression)
    # "difficult" — receives filler by default; use real items with DifficultMonsters option on
    game_stage: str = "mid"


# ==================== VIEW MILESTONE TABLE ====================
# Per-day lifetime-views milestones (canonical, from Jake's spreadsheet).
# (day, lifetime_total_views, quota_number).  Source of truth for both the
# locations generated below and the access rules in rules.py.
VIEW_MILESTONES: List[Tuple[int, int, int]] = [
    (1,  1_000,      1), (2,  2_000,      1), (3,  3_000,      1),
    (4,  16_000,     2), (5,  29_000,     2), (6,  42_000,     2),
    (7,  84_667,     3), (8,  127_333,    3), (9,  170_000,    3),
    (10, 278_333,    4), (11, 386_667,    4), (12, 495_000,    4),
    (13, 709_667,    5), (14, 924_333,    5), (15, 1_139_000,  5),
    (16, 1_505_667,  6), (17, 1_872_333,  6), (18, 2_239_000,  6),
    (19, 2_839_000,  7), (20, 3_439_000,  7), (21, 4_039_000,  7),
    (22, 4_639_000,  8), (23, 5_239_000,  8), (24, 5_839_000,  8),
    (25, 6_472_333,  9), (26, 7_105_667,  9), (27, 7_739_000,  9),
    (28, 8_372_333, 10), (29, 9_005_667, 10), (30, 9_639_000, 10),
    (31, 10_305_667, 11), (32, 10_972_333, 11), (33, 11_639_000, 11),
    (34, 12_305_667, 12), (35, 12_972_333, 12), (36, 13_639_000, 12),
    (37, 14_305_667, 13), (38, 14_972_333, 13), (39, 15_639_000, 13),
    (40, 16_339_000, 14), (41, 17_039_000, 14), (42, 17_739_000, 14),
    (43, 18_439_000, 15), (44, 19_139_000, 15), (45, 19_839_000, 15),
    (46, 20_572_333, 16), (47, 21_305_667, 16), (48, 22_039_000, 16),
    (49, 22_772_333, 17), (50, 23_505_667, 17), (51, 24_239_000, 17),
    (52, 25_005_667, 18), (53, 25_772_333, 18), (54, 26_539_000, 18),
    (55, 27_305_667, 19), (56, 28_072_333, 19), (57, 28_839_000, 19),
    (58, 29_639_000, 20), (59, 30_439_000, 20), (60, 31_239_000, 20),
    (61, 32_072_333, 21), (62, 32_905_667, 21), (63, 33_739_000, 21),
]

# Lookup: day -> lifetime_total
LIFETIME_VIEWS_BY_DAY: Dict[int, int] = {day: total for day, total, _ in VIEW_MILESTONES}

# Maximum lifetime total across the table — also the upper bound of
# ViewsGoalTarget in options.py.
MAX_LIFETIME_VIEWS: int = VIEW_MILESTONES[-1][1]


def _view_stage_for_quota(quota: int) -> str:
    """Map a quota number to a coarse game_stage for AP item-classification
    distribution purposes.  Q1 is early, Q2-3 mid, Q4+ late."""
    if quota == 1:
        return "early"
    if quota <= 3:
        return "mid"
    return "late"


def _day_stage_for_day(day: int) -> str:
    """Map an extraction day to a coarse game_stage."""
    if day <= 5:
        return "early"
    if day <= 10:
        return "mid"
    return "late"


# Difficult monsters — duplicated from the location entries below so we can
# resolve "is this monster difficult?" by base name when classifying tiers.
_DIFFICULT_MONSTERS: Set[str] = {
    "Filmed Weeping",
    "Filmed Flicker",
    "Filmed Cam Creep",
    "Filmed Infiltrator",
    "Filmed Black Hole Bot",
    "Filmed Ear",
    "Filmed Snail Spawner",
    "Filmed Big Slap",
    "Filmed Ultra Knifo",
}


# ==================== LOCATION TABLE ====================
location_table: Dict[str, CWLocationData] = {

    # ==================== BASIC EXTRACTION & DAY CHECKS ====================
    lname.any_extraction: CWLocationData(rname.dungeon, 0, "Extractions", "early"),
}

# Day extractions: 1..63 at offsets 1..63.  create_regions filters to
# QuotaCount * 3 per generation.
for _d in range(1, 64):
    location_table[lname.extracted_footage_prefix + str(_d)] = CWLocationData(
        rname.hub, _d, "Days", _day_stage_for_day(_d)
    )

# ==================== QUOTA CHECKS ====================
# Up to 21 quotas; create_regions only creates locations up to QuotaCount.
for _q in range(1, 22):
    _stage = "early" if _q <= 2 else "mid" if _q <= 4 else "late"
    location_table[lname.met_quota_prefix + str(_q)] = CWLocationData(
        rname.hub, 99 + _q, "Quotas", _stage
    )

# ==================== VIEW MILESTONES ====================
# Generated from VIEW_MILESTONES.  Offsets 200..262 (one per day).
for _day, _total, _quota in VIEW_MILESTONES:
    location_table[lname.reached_total_views(_total)] = CWLocationData(
        rname.hub, 199 + _day, "Views", _view_stage_for_quota(_quota)
    )

# ==================== MONSTER FILMING CHECKS ====================
location_table.update({
    # Early game monsters
    "Filmed Slurper":       CWLocationData(rname.dungeon, 300, "Monsters", "early"),
    "Filmed Zombe":         CWLocationData(rname.dungeon, 301, "Monsters", "early"),
    "Filmed Button Robot":  CWLocationData(rname.dungeon, 307, "Monsters", "early"),
    "Filmed Puffo":         CWLocationData(rname.dungeon, 308, "Monsters", "early"),
    "Filmed Whisk":         CWLocationData(rname.dungeon, 311, "Monsters", "early"),
    "Filmed Arms":          CWLocationData(rname.dungeon, 322, "Monsters", "early"),

    # Mid game monsters
    "Filmed Worm":          CWLocationData(rname.dungeon, 302, "Monsters", "mid"),
    "Filmed Mouthe":        CWLocationData(rname.dungeon, 303, "Monsters", "mid"),
    "Filmed Spider":        CWLocationData(rname.dungeon, 312, "Monsters", "mid"),
    "Filmed Bomber":        CWLocationData(rname.dungeon, 316, "Monsters", "mid"),
    "Filmed Dog":           CWLocationData(rname.dungeon, 317, "Monsters", "mid"),
    "Filmed Eye Guy":       CWLocationData(rname.dungeon, 318, "Monsters", "mid"),
    "Filmed Knifo":         CWLocationData(rname.dungeon, 320, "Monsters", "mid"),
    "Filmed Larva":         CWLocationData(rname.dungeon, 321, "Monsters", "mid"),
    "Filmed Harpooner":     CWLocationData(rname.dungeon, 323, "Monsters", "mid"),
    "Filmed Barnacle Ball": CWLocationData(rname.dungeon, 325, "Monsters", "mid"),

    # Late game monsters
    "Filmed Snatcho":       CWLocationData(rname.dungeon, 310, "Monsters", "late"),
    "Filmed Jelly":         CWLocationData(rname.dungeon, 314, "Monsters", "late"),
    "Filmed Fire":          CWLocationData(rname.dungeon, 319, "Monsters", "late"),
    "Filmed Mime":          CWLocationData(rname.dungeon, 324, "Monsters", "late"),
    "Filmed Streamer":      CWLocationData(rname.dungeon, 328, "Monsters", "late"),

    # Difficult monsters — filler by default; DifficultMonsters option enables real items
    # Weeping is also multiplayer-only (see __init__.py / rules.py).
    "Filmed Weeping":       CWLocationData(rname.dungeon, 315, "Monsters", "difficult"),
    "Filmed Flicker":       CWLocationData(rname.dungeon, 304, "Monsters", "difficult"),
    "Filmed Cam Creep":     CWLocationData(rname.dungeon, 305, "Monsters", "difficult"),
    "Filmed Infiltrator":   CWLocationData(rname.dungeon, 306, "Monsters", "difficult"),
    "Filmed Black Hole Bot":CWLocationData(rname.dungeon, 309, "Monsters", "difficult"),
    "Filmed Ear":           CWLocationData(rname.dungeon, 313, "Monsters", "difficult"),
    "Filmed Snail Spawner": CWLocationData(rname.dungeon, 326, "Monsters", "difficult"),
    "Filmed Big Slap":      CWLocationData(rname.dungeon, 327, "Monsters", "difficult"),
    "Filmed Ultra Knifo":   CWLocationData(rname.dungeon, 329, "Monsters", "difficult"),

    # ==================== TIERED MONSTER FILMING (optional) ====================
    # Tier 2 / Tier 3 — only created when MonsterTiers is on.

    # ── Tier 2 (offsets 330–350) ─────────────────────────────────────────────
    "Filmed Slurper 2":         CWLocationData(rname.dungeon, 330, "Monster Tiers", "early"),
    "Filmed Zombe 2":           CWLocationData(rname.dungeon, 331, "Monster Tiers", "early"),
    "Filmed Button Robot 2":    CWLocationData(rname.dungeon, 332, "Monster Tiers", "early"),
    "Filmed Puffo 2":           CWLocationData(rname.dungeon, 333, "Monster Tiers", "early"),
    "Filmed Whisk 2":           CWLocationData(rname.dungeon, 334, "Monster Tiers", "early"),
    "Filmed Arms 2":            CWLocationData(rname.dungeon, 335, "Monster Tiers", "early"),
    "Filmed Worm 2":            CWLocationData(rname.dungeon, 336, "Monster Tiers", "mid"),
    "Filmed Mouthe 2":          CWLocationData(rname.dungeon, 337, "Monster Tiers", "mid"),
    "Filmed Spider 2":          CWLocationData(rname.dungeon, 338, "Monster Tiers", "mid"),
    "Filmed Bomber 2":          CWLocationData(rname.dungeon, 339, "Monster Tiers", "mid"),
    "Filmed Dog 2":             CWLocationData(rname.dungeon, 340, "Monster Tiers", "mid"),
    "Filmed Eye Guy 2":         CWLocationData(rname.dungeon, 341, "Monster Tiers", "mid"),
    "Filmed Knifo 2":           CWLocationData(rname.dungeon, 342, "Monster Tiers", "mid"),
    "Filmed Larva 2":           CWLocationData(rname.dungeon, 343, "Monster Tiers", "mid"),
    "Filmed Harpooner 2":       CWLocationData(rname.dungeon, 344, "Monster Tiers", "mid"),
    "Filmed Barnacle Ball 2":   CWLocationData(rname.dungeon, 345, "Monster Tiers", "mid"),
    "Filmed Snatcho 2":         CWLocationData(rname.dungeon, 346, "Monster Tiers", "late"),
    "Filmed Jelly 2":           CWLocationData(rname.dungeon, 347, "Monster Tiers", "late"),
    "Filmed Fire 2":            CWLocationData(rname.dungeon, 348, "Monster Tiers", "late"),
    "Filmed Mime 2":            CWLocationData(rname.dungeon, 349, "Monster Tiers", "late"),
    "Filmed Streamer 2":        CWLocationData(rname.dungeon, 350, "Monster Tiers", "late"),

    # ── Tier 3 (offsets 351–371) ─────────────────────────────────────────────
    "Filmed Slurper 3":         CWLocationData(rname.dungeon, 351, "Monster Tiers", "late"),
    "Filmed Zombe 3":           CWLocationData(rname.dungeon, 352, "Monster Tiers", "late"),
    "Filmed Button Robot 3":    CWLocationData(rname.dungeon, 353, "Monster Tiers", "late"),
    "Filmed Puffo 3":           CWLocationData(rname.dungeon, 354, "Monster Tiers", "late"),
    "Filmed Whisk 3":           CWLocationData(rname.dungeon, 355, "Monster Tiers", "late"),
    "Filmed Arms 3":            CWLocationData(rname.dungeon, 356, "Monster Tiers", "late"),
    "Filmed Worm 3":            CWLocationData(rname.dungeon, 357, "Monster Tiers", "late"),
    "Filmed Mouthe 3":          CWLocationData(rname.dungeon, 358, "Monster Tiers", "late"),
    "Filmed Spider 3":          CWLocationData(rname.dungeon, 359, "Monster Tiers", "late"),
    "Filmed Bomber 3":          CWLocationData(rname.dungeon, 360, "Monster Tiers", "late"),
    "Filmed Dog 3":             CWLocationData(rname.dungeon, 361, "Monster Tiers", "late"),
    "Filmed Eye Guy 3":         CWLocationData(rname.dungeon, 362, "Monster Tiers", "late"),
    "Filmed Knifo 3":           CWLocationData(rname.dungeon, 363, "Monster Tiers", "late"),
    "Filmed Larva 3":           CWLocationData(rname.dungeon, 364, "Monster Tiers", "late"),
    "Filmed Harpooner 3":       CWLocationData(rname.dungeon, 365, "Monster Tiers", "late"),
    "Filmed Barnacle Ball 3":   CWLocationData(rname.dungeon, 366, "Monster Tiers", "late"),
    "Filmed Snatcho 3":         CWLocationData(rname.dungeon, 367, "Monster Tiers", "late"),
    "Filmed Jelly 3":           CWLocationData(rname.dungeon, 368, "Monster Tiers", "late"),
    "Filmed Fire 3":            CWLocationData(rname.dungeon, 369, "Monster Tiers", "late"),
    "Filmed Mime 3":            CWLocationData(rname.dungeon, 370, "Monster Tiers", "late"),
    "Filmed Streamer 3":        CWLocationData(rname.dungeon, 371, "Monster Tiers", "late"),

    # ==================== ARTIFACT FILMING CHECKS ====================
    # Early / mid game artifacts
    "Filmed Ribcage":       CWLocationData(rname.dungeon, 400, "Artifacts", "early"),
    "Filmed Skull":         CWLocationData(rname.dungeon, 401, "Artifacts", "early"),
    "Filmed Spine":         CWLocationData(rname.dungeon, 402, "Artifacts", "early"),
    "Filmed Bone":          CWLocationData(rname.dungeon, 403, "Artifacts", "early"),
    "Filmed Apple":         CWLocationData(rname.dungeon, 411, "Artifacts", "mid"),

    # Filler artifacts — always receive filler items
    "Filmed Brain on a Stick":      CWLocationData(rname.dungeon, 404, "Artifacts", "filler"),
    "Filmed Radio":                 CWLocationData(rname.dungeon, 405, "Artifacts", "filler"),
    "Filmed Shroom":                CWLocationData(rname.dungeon, 406, "Artifacts", "filler"),
    "Filmed Animal Statues":        CWLocationData(rname.dungeon, 407, "Artifacts", "filler"),
    "Filmed Radioactive Container": CWLocationData(rname.dungeon, 408, "Artifacts", "filler"),
    "Filmed Old Painting":          CWLocationData(rname.dungeon, 409, "Artifacts", "filler"),
    "Filmed Chorby":                CWLocationData(rname.dungeon, 410, "Artifacts", "filler"),

    # Filming equipment item in the dungeon
    "Filmed Reporter Mic":  CWLocationData(rname.dungeon, 412, "Artifacts", "early"),

    # ==================== ARTIFACT FILMING TIERS (optional) ====================
    # Same gate as monster tiers (MonsterTiers option).

    # ── Artifact Tier 2 (offsets 413–425) ────────────────────────────────────
    "Filmed Ribcage 2":               CWLocationData(rname.dungeon, 413, "Monster Tiers", "early"),
    "Filmed Skull 2":                 CWLocationData(rname.dungeon, 414, "Monster Tiers", "early"),
    "Filmed Spine 2":                 CWLocationData(rname.dungeon, 415, "Monster Tiers", "early"),
    "Filmed Bone 2":                  CWLocationData(rname.dungeon, 416, "Monster Tiers", "early"),
    "Filmed Brain on a Stick 2":      CWLocationData(rname.dungeon, 417, "Monster Tiers", "filler"),
    "Filmed Radio 2":                 CWLocationData(rname.dungeon, 418, "Monster Tiers", "filler"),
    "Filmed Shroom 2":                CWLocationData(rname.dungeon, 419, "Monster Tiers", "filler"),
    "Filmed Animal Statues 2":        CWLocationData(rname.dungeon, 420, "Monster Tiers", "filler"),
    "Filmed Radioactive Container 2": CWLocationData(rname.dungeon, 421, "Monster Tiers", "filler"),
    "Filmed Old Painting 2":          CWLocationData(rname.dungeon, 422, "Monster Tiers", "filler"),
    "Filmed Chorby 2":                CWLocationData(rname.dungeon, 423, "Monster Tiers", "filler"),
    "Filmed Apple 2":                 CWLocationData(rname.dungeon, 424, "Monster Tiers", "mid"),
    "Filmed Reporter Mic 2":          CWLocationData(rname.dungeon, 425, "Monster Tiers", "early"),

    # ── Artifact Tier 3 (offsets 426–438) ────────────────────────────────────
    "Filmed Ribcage 3":               CWLocationData(rname.dungeon, 426, "Monster Tiers", "late"),
    "Filmed Skull 3":                 CWLocationData(rname.dungeon, 427, "Monster Tiers", "late"),
    "Filmed Spine 3":                 CWLocationData(rname.dungeon, 428, "Monster Tiers", "late"),
    "Filmed Bone 3":                  CWLocationData(rname.dungeon, 429, "Monster Tiers", "late"),
    "Filmed Brain on a Stick 3":      CWLocationData(rname.dungeon, 430, "Monster Tiers", "filler"),
    "Filmed Radio 3":                 CWLocationData(rname.dungeon, 431, "Monster Tiers", "filler"),
    "Filmed Shroom 3":                CWLocationData(rname.dungeon, 432, "Monster Tiers", "filler"),
    "Filmed Animal Statues 3":        CWLocationData(rname.dungeon, 433, "Monster Tiers", "filler"),
    "Filmed Radioactive Container 3": CWLocationData(rname.dungeon, 434, "Monster Tiers", "filler"),
    "Filmed Old Painting 3":          CWLocationData(rname.dungeon, 435, "Monster Tiers", "filler"),
    "Filmed Chorby 3":                CWLocationData(rname.dungeon, 436, "Monster Tiers", "filler"),
    "Filmed Apple 3":                 CWLocationData(rname.dungeon, 437, "Monster Tiers", "late"),
    "Filmed Reporter Mic 3":          CWLocationData(rname.dungeon, 438, "Monster Tiers", "late"),

    # ==================== STORE PURCHASE CHECKS ====================
    # Early game store purchases
    "Bought Old Flashlight":  CWLocationData(rname.hub, 500, "Store Purchases", "early"),
    "Bought Flare":           CWLocationData(rname.hub, 501, "Store Purchases", "early"),
    "Bought Reporter Mic":    CWLocationData(rname.hub, 508, "Store Purchases", "early"),
    "Bought Boom Mic":        CWLocationData(rname.hub, 509, "Store Purchases", "early"),
    "Bought Clapper":         CWLocationData(rname.hub, 510, "Store Purchases", "early"),
    "Bought Sound Player":    CWLocationData(rname.hub, 511, "Store Purchases", "early"),
    "Bought Goo Ball":        CWLocationData(rname.hub, 512, "Store Purchases", "early"),
    "Bought Party Popper":    CWLocationData(rname.hub, 570, "Store Purchases", "early"),

    # Mid game store purchases
    "Bought Modern Flashlight": CWLocationData(rname.hub, 502, "Store Purchases", "mid"),
    "Bought Long Flashlight":   CWLocationData(rname.hub, 503, "Store Purchases", "mid"),
    "Bought Hugger":            CWLocationData(rname.hub, 506, "Store Purchases", "mid"),
    "Bought Rescue Hook":       CWLocationData(rname.hub, 513, "Store Purchases", "mid"),
    "Bought Sketch Pad":        CWLocationData(rname.hub, 515, "Store Purchases", "mid"),

    # Late game store purchases
    "Bought Modern Flashlight Pro": CWLocationData(rname.hub, 504, "Store Purchases", "late"),
    "Bought Long Flashlight Pro":   CWLocationData(rname.hub, 505, "Store Purchases", "late"),
    "Bought Defibrillator":         CWLocationData(rname.hub, 507, "Store Purchases", "late"),
    "Bought Shock Stick":           CWLocationData(rname.hub, 514, "Store Purchases", "late"),

    # ==================== EMOTE CHECKS ====================
    # Early game emotes
    "Bought Applause":           CWLocationData(rname.hub, 550, "Emotes", "early"),
    "Bought Workout 1":          CWLocationData(rname.hub, 551, "Emotes", "early"),
    "Bought Confused":           CWLocationData(rname.hub, 552, "Emotes", "early"),
    "Bought Dance 103":          CWLocationData(rname.hub, 553, "Emotes", "early"),
    "Bought Caring":             CWLocationData(rname.hub, 558, "Emotes", "early"),
    "Bought Ancient Gestures 3": CWLocationData(rname.hub, 559, "Emotes", "early"),
    "Bought Ancient Gestures 2": CWLocationData(rname.hub, 560, "Emotes", "early"),

    # Mid game emotes
    "Bought Dance 102":          CWLocationData(rname.hub, 554, "Emotes", "mid"),
    "Bought Dance 101":          CWLocationData(rname.hub, 555, "Emotes", "mid"),
    "Bought Backflip":           CWLocationData(rname.hub, 556, "Emotes", "mid"),
    "Bought Yoga":               CWLocationData(rname.hub, 561, "Emotes", "mid"),
    "Bought Workout 2":          CWLocationData(rname.hub, 562, "Emotes", "mid"),

    # Late game emotes
    "Bought Gymnastics":         CWLocationData(rname.hub, 557, "Emotes", "late"),
    "Bought Thumbnail 1":        CWLocationData(rname.hub, 563, "Emotes", "late"),
    "Bought Thumbnail 2":        CWLocationData(rname.hub, 564, "Emotes", "late"),
    "Bought Ancient Gestures 1": CWLocationData(rname.hub, 565, "Emotes", "late"),

    # ==================== HAT CHECKS ====================
    # Early game hats
    "Bought Beanie":        CWLocationData(rname.hub, 601, "Hats", "early"),
    "Bought Bucket Hat":    CWLocationData(rname.hub, 602, "Hats", "early"),
    "Bought Floppy Hat":    CWLocationData(rname.hub, 605, "Hats", "early"),
    "Bought Homburg":       CWLocationData(rname.hub, 606, "Hats", "early"),
    "Bought Bowler Hat":    CWLocationData(rname.hub, 608, "Hats", "early"),
    "Bought Cap":           CWLocationData(rname.hub, 609, "Hats", "early"),
    "Bought News Cap":      CWLocationData(rname.hub, 620, "Hats", "early"),
    "Bought Sports Helmet": CWLocationData(rname.hub, 622, "Hats", "early"),
    "Bought Hard Hat":      CWLocationData(rname.hub, 629, "Hats", "early"),

    # Mid game hats
    "Bought Chefs Hat":     CWLocationData(rname.hub, 604, "Hats", "mid"),
    "Bought Propeller Hat": CWLocationData(rname.hub, 610, "Hats", "mid"),
    "Bought Cowboy Hat":    CWLocationData(rname.hub, 612, "Hats", "mid"),
    "Bought Horns":         CWLocationData(rname.hub, 615, "Hats", "mid"),
    "Bought Hotdog Hat":    CWLocationData(rname.hub, 616, "Hats", "mid"),
    "Bought Milk Hat":      CWLocationData(rname.hub, 619, "Hats", "mid"),
    "Bought Pirate Hat":    CWLocationData(rname.hub, 621, "Hats", "mid"),
    "Bought Top Hat":       CWLocationData(rname.hub, 624, "Hats", "mid"),
    "Bought Party Hat":     CWLocationData(rname.hub, 625, "Hats", "mid"),
    "Bought Ushanka":       CWLocationData(rname.hub, 627, "Hats", "mid"),

    # Late game hats
    "Bought Balaclava":     CWLocationData(rname.hub, 600, "Hats", "late"),
    "Bought Cat Ears":      CWLocationData(rname.hub, 603, "Hats", "late"),
    "Bought Curly Hair":    CWLocationData(rname.hub, 607, "Hats", "late"),
    "Bought Clown Hair":    CWLocationData(rname.hub, 611, "Hats", "late"),
    "Bought Crown":         CWLocationData(rname.hub, 613, "Hats", "late"),
    "Bought Halo":          CWLocationData(rname.hub, 614, "Hats", "late"),
    "Bought Jesters Hat":   CWLocationData(rname.hub, 617, "Hats", "late"),
    "Bought Ghost Hat":     CWLocationData(rname.hub, 618, "Hats", "late"),
    "Bought Tooop Hat":     CWLocationData(rname.hub, 623, "Hats", "late"),
    "Bought Shroom Hat":    CWLocationData(rname.hub, 626, "Hats", "late"),
    "Bought Witch Hat":     CWLocationData(rname.hub, 628, "Hats", "late"),
    "Bought Savannah Hair": CWLocationData(rname.hub, 630, "Hats", "late"),

    # ==================== VIRAL SENSATION (client event) ====================
    # Fired by the client when the player crosses 1,000,000 views in a single
    # quota.  Created in the world only when the viral_sensation goal is on.
    lname.viral_sensation_achieved: CWLocationData(rname.hub, 800, "Viral Sensation", "late"),

    # ==================== VICTORY (EVENT) ====================
    lname.victory: CWLocationData(rname.hub, None, "Event", "late"),
})

# ==================== SPONSORSHIP CHECKS ====================
# Up to 20 sponsorship completion checks; create_regions activates only
# QuotaCount - 1 of them (capped at 20).  Trigger is per-completion mod-side
# (issue #5 Q3).  Persisted across runs by the mod so failed runs don't
# reset the counter.
for _s in range(1, 21):
    _stage = "mid" if _s <= 4 else "late"
    location_table[lname.completed_sponsorship_prefix + str(_s)] = CWLocationData(
        rname.hub, 699 + _s, "Sponsorships", _stage
    )

# ==================== COMPUTED LOOKUPS ====================
location_name_to_id: Dict[str, Optional[int]] = {}

for _loc_name, _loc_data in location_table.items():
    if _loc_data.location_id_offset is not None:
        location_name_to_id[_loc_name] = location_base_id + _loc_data.location_id_offset
    else:
        location_name_to_id[_loc_name] = None


# All non-event locations (used as the ceiling for pool balancing).
# __init__.py adjusts this downward based on disabled option groups.
location_total: int = sum(
    1 for data in location_table.values()
    if data.location_id_offset is not None
)

# ==================== LOCATION NAME GROUPS ====================
location_name_groups: Dict[str, Set[str]] = {
    "Days": {
        lname.extracted_footage_prefix + str(i) for i in range(1, 64)
    },
    "Quotas": {
        lname.met_quota_prefix + str(i) for i in range(1, 22)
    },
    "Views": {
        name for name in location_table if location_table[name].location_group == "Views"
    },
    "Monsters": {
        name for name in location_table if location_table[name].location_group == "Monsters"
    },
    "Monster Tiers": {
        name for name in location_table if location_table[name].location_group == "Monster Tiers"
    },
    "Artifacts": {
        name for name in location_table if location_table[name].location_group == "Artifacts"
    },
    "Store Purchases": {
        name for name in location_table if location_table[name].location_group == "Store Purchases"
    },
    "Emotes": {
        name for name in location_table if location_table[name].location_group == "Emotes"
    },
    "Hats": {
        name for name in location_table if location_table[name].location_group == "Hats"
    },
    "Sponsorships": {
        name for name in location_table if location_table[name].location_group == "Sponsorships"
    },
    "Extractions": {
        name for name in location_table if location_table[name].location_group == "Extractions"
    },
    "Viral Sensation": {
        name for name in location_table if location_table[name].location_group == "Viral Sensation"
    },
}
