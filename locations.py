# worlds/content_warning/locations.py

from typing import Dict, Optional, Set, NamedTuple
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


# ==================== LOCATION TABLE ====================
# region key:
#   rname.hub     — Sky Island (extractions, quotas, views, shop, hats, emotes, sponsorships)
#   rname.dungeon — The Old World (monster / artifact filming)
location_table: Dict[str, CWLocationData] = {

    # ==================== BASIC EXTRACTION & DAY CHECKS ====================
    lname.any_extraction: CWLocationData(rname.dungeon, 0, "Extractions", "early"),

    lname.extracted_footage_prefix + "1":  CWLocationData(rname.hub,  1, "Days", "early"),
    lname.extracted_footage_prefix + "2":  CWLocationData(rname.hub,  2, "Days", "early"),
    lname.extracted_footage_prefix + "3":  CWLocationData(rname.hub,  3, "Days", "early"),
    lname.extracted_footage_prefix + "4":  CWLocationData(rname.hub,  4, "Days", "early"),
    lname.extracted_footage_prefix + "5":  CWLocationData(rname.hub,  5, "Days", "early"),
    lname.extracted_footage_prefix + "6":  CWLocationData(rname.hub,  6, "Days", "mid"),
    lname.extracted_footage_prefix + "7":  CWLocationData(rname.hub,  7, "Days", "mid"),
    lname.extracted_footage_prefix + "8":  CWLocationData(rname.hub,  8, "Days", "mid"),
    lname.extracted_footage_prefix + "9":  CWLocationData(rname.hub,  9, "Days", "mid"),
    lname.extracted_footage_prefix + "10": CWLocationData(rname.hub, 10, "Days", "mid"),
    lname.extracted_footage_prefix + "11": CWLocationData(rname.hub, 11, "Days", "late"),
    lname.extracted_footage_prefix + "12": CWLocationData(rname.hub, 12, "Days", "late"),
    lname.extracted_footage_prefix + "13": CWLocationData(rname.hub, 13, "Days", "late"),
    lname.extracted_footage_prefix + "14": CWLocationData(rname.hub, 14, "Days", "late"),
    lname.extracted_footage_prefix + "15": CWLocationData(rname.hub, 15, "Days", "late"),

    # ==================== QUOTA CHECKS ====================
    # Up to 10 quotas; __init__.py only creates locations up to the configured quota count.
    lname.met_quota_prefix + "1":  CWLocationData(rname.hub, 100, "Quotas", "early"),
    lname.met_quota_prefix + "2":  CWLocationData(rname.hub, 101, "Quotas", "early"),
    lname.met_quota_prefix + "3":  CWLocationData(rname.hub, 102, "Quotas", "mid"),
    lname.met_quota_prefix + "4":  CWLocationData(rname.hub, 103, "Quotas", "mid"),
    lname.met_quota_prefix + "5":  CWLocationData(rname.hub, 104, "Quotas", "late"),
    lname.met_quota_prefix + "6":  CWLocationData(rname.hub, 105, "Quotas", "late"),
    lname.met_quota_prefix + "7":  CWLocationData(rname.hub, 106, "Quotas", "late"),
    lname.met_quota_prefix + "8":  CWLocationData(rname.hub, 107, "Quotas", "late"),
    lname.met_quota_prefix + "9":  CWLocationData(rname.hub, 108, "Quotas", "late"),
    lname.met_quota_prefix + "10": CWLocationData(rname.hub, 109, "Quotas", "late"),

    # ==================== VIEW MILESTONES ====================
    lname.reached_1k:   CWLocationData(rname.hub, 200, "Views", "early"),
    lname.reached_2k:   CWLocationData(rname.hub, 201, "Views", "early"),
    lname.reached_3k:   CWLocationData(rname.hub, 202, "Views", "early"),
    lname.reached_13k:  CWLocationData(rname.hub, 203, "Views", "early"),
    lname.reached_26k:  CWLocationData(rname.hub, 204, "Views", "early"),
    lname.reached_39k:  CWLocationData(rname.hub, 205, "Views", "mid"),
    lname.reached_43k:  CWLocationData(rname.hub, 206, "Views", "mid"),
    lname.reached_85k:  CWLocationData(rname.hub, 207, "Views", "mid"),
    lname.reached_128k: CWLocationData(rname.hub, 208, "Views", "mid"),
    lname.reached_150k: CWLocationData(rname.hub, 209, "Views", "late"),
    lname.reached_220k: CWLocationData(rname.hub, 210, "Views", "late"),
    lname.reached_325k: CWLocationData(rname.hub, 211, "Views", "late"),
    lname.reached_375k: CWLocationData(rname.hub, 212, "Views", "late"),
    lname.reached_430k: CWLocationData(rname.hub, 213, "Views", "late"),
    lname.reached_645k: CWLocationData(rname.hub, 214, "Views", "late"),
    lname.reached_850k: CWLocationData(rname.hub, 215, "Views", "late"),
    lname.reached_1m:   CWLocationData(rname.hub, 216, "Views", "late"),

    # ==================== MONSTER FILMING CHECKS ====================
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
    "Filmed Dog":           CWLocationData(rname.dungeon, 317, "Monsters", "mid"),  # Robot Dog
    "Filmed Eye Guy":       CWLocationData(rname.dungeon, 318, "Monsters", "mid"),
    "Filmed Knifo":         CWLocationData(rname.dungeon, 320, "Monsters", "mid"),
    "Filmed Larva":         CWLocationData(rname.dungeon, 321, "Monsters", "mid"),  # was Grabber Snake
    "Filmed Harpooner":     CWLocationData(rname.dungeon, 323, "Monsters", "mid"),
    "Filmed Barnacle Ball": CWLocationData(rname.dungeon, 325, "Monsters", "mid"),

    # Late game monsters
    "Filmed Snatcho":       CWLocationData(rname.dungeon, 310, "Monsters", "late"),
    "Filmed Jelly":         CWLocationData(rname.dungeon, 314, "Monsters", "late"),
    "Filmed Fire":          CWLocationData(rname.dungeon, 319, "Monsters", "late"),
    "Filmed Mime":          CWLocationData(rname.dungeon, 324, "Monsters", "late"),
    "Filmed Streamer":      CWLocationData(rname.dungeon, 328, "Monsters", "late"),

    # Difficult monsters — filler by default; DifficultMonsters option can enable real items
    # Weeping is also multiplayer-only (see rules.py and MultiplayerMode option).
    "Filmed Weeping":       CWLocationData(rname.dungeon, 315, "Monsters", "difficult"),  # Iron Maiden / Wheeping
    "Filmed Flicker":       CWLocationData(rname.dungeon, 304, "Monsters", "difficult"),
    "Filmed Cam Creep":     CWLocationData(rname.dungeon, 305, "Monsters", "difficult"),
    "Filmed Infiltrator":   CWLocationData(rname.dungeon, 306, "Monsters", "difficult"),
    "Filmed Black Hole Bot":CWLocationData(rname.dungeon, 309, "Monsters", "difficult"),
    "Filmed Ear":           CWLocationData(rname.dungeon, 313, "Monsters", "difficult"),
    "Filmed Snail Spawner": CWLocationData(rname.dungeon, 326, "Monsters", "difficult"),
    "Filmed Big Slap":      CWLocationData(rname.dungeon, 327, "Monsters", "difficult"),
    "Filmed Ultra Knifo":   CWLocationData(rname.dungeon, 329, "Monsters", "difficult"),

    # ==================== TIERED MONSTER FILMING (optional) ====================
    # Enabled by the MonsterTiers option.
    # Tier 1 = base checks above (unchanged).
    # Tier 2 preserves the base monster's game_stage so dungeon-depth rules apply
    # automatically from the existing stage loop in rules.py.
    # Tier 3 uses "late" stage — requires best exploration capability for any monster.
    # Does not include difficult monsters (Flicker, Cam Creep, etc., Weeping).
    # Worm tiers are included here but are still subject to the MultiplhayerMode rule
    # applied to the base "Filmed Worm" location in rules.py.

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

    # ── Tier 3 (offsets 351–371) — all "late" stage ───────────────────────────
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
    "Bought News Cap":      CWLocationData(rname.hub, 620, "Hats", "early"),  # Newsboy Cap
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

    # ==================== SPONSORSHIP CHECKS ====================
    # 3 checks for accepting sponsorships (base, always in pool)
    lname.accepted_sponsorship_prefix + "1": CWLocationData(rname.hub, 700, "Sponsorships", "mid"),
    lname.accepted_sponsorship_prefix + "2": CWLocationData(rname.hub, 701, "Sponsorships", "mid"),
    lname.accepted_sponsorship_prefix + "3": CWLocationData(rname.hub, 702, "Sponsorships", "late"),

    # Completion checks — only active when Sponsorsanity option is enabled
    lname.completed_sponsorship_prefix + "Easy":      CWLocationData(rname.hub, 703, "Sponsorsanity", "mid"),
    lname.completed_sponsorship_prefix + "Medium":    CWLocationData(rname.hub, 704, "Sponsorsanity", "mid"),
    lname.completed_sponsorship_prefix + "Hard":      CWLocationData(rname.hub, 705, "Sponsorsanity", "late"),
    lname.completed_sponsorship_prefix + "Very Hard": CWLocationData(rname.hub, 706, "Sponsorsanity", "late"),

    # ==================== VICTORY (EVENT) ====================
    lname.victory: CWLocationData(rname.hub, None, "Event", "late"),
}

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
        lname.extracted_footage_prefix + str(i) for i in range(1, 16)
    },
    "Quotas": {
        lname.met_quota_prefix + str(i) for i in range(1, 11)
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
    "Sponsorsanity": {
        name for name in location_table if location_table[name].location_group == "Sponsorsanity"
    },
    "Extractions": {
        name for name in location_table if location_table[name].location_group == "Extractions"
    },
}
