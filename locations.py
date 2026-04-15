# worlds/content_warning/locations.py

from typing import Dict, List, Optional, Set, NamedTuple
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


# ==================== LOCATION TABLE ====================
# region key:
#   rname.hub     — island surface (extractions, quotas, views, shop, hats, emotes, sponsorships)
#   rname.dungeon — underground facility (monster / artifact filming)
location_table: Dict[str, CWLocationData] = {

    # ==================== BASIC EXTRACTION & DAY CHECKS ====================
    lname.any_extraction: CWLocationData(rname.dungeon, 0, "Extractions"),

    lname.extracted_footage_prefix + "1":  CWLocationData(rname.hub,  1, "Days"),
    lname.extracted_footage_prefix + "2":  CWLocationData(rname.hub,  2, "Days"),
    lname.extracted_footage_prefix + "3":  CWLocationData(rname.hub,  3, "Days"),
    lname.extracted_footage_prefix + "4":  CWLocationData(rname.hub,  4, "Days"),
    lname.extracted_footage_prefix + "5":  CWLocationData(rname.hub,  5, "Days"),
    lname.extracted_footage_prefix + "6":  CWLocationData(rname.hub,  6, "Days"),
    lname.extracted_footage_prefix + "7":  CWLocationData(rname.hub,  7, "Days"),
    lname.extracted_footage_prefix + "8":  CWLocationData(rname.hub,  8, "Days"),
    lname.extracted_footage_prefix + "9":  CWLocationData(rname.hub,  9, "Days"),
    lname.extracted_footage_prefix + "10": CWLocationData(rname.hub, 10, "Days"),
    lname.extracted_footage_prefix + "11": CWLocationData(rname.hub, 11, "Days"),
    lname.extracted_footage_prefix + "12": CWLocationData(rname.hub, 12, "Days"),
    lname.extracted_footage_prefix + "13": CWLocationData(rname.hub, 13, "Days"),
    lname.extracted_footage_prefix + "14": CWLocationData(rname.hub, 14, "Days"),
    lname.extracted_footage_prefix + "15": CWLocationData(rname.hub, 15, "Days"),

    # ==================== QUOTA CHECKS ====================
    lname.met_quota_prefix + "1": CWLocationData(rname.hub, 100, "Quotas"),
    lname.met_quota_prefix + "2": CWLocationData(rname.hub, 101, "Quotas"),
    lname.met_quota_prefix + "3": CWLocationData(rname.hub, 102, "Quotas"),
    lname.met_quota_prefix + "4": CWLocationData(rname.hub, 103, "Quotas"),
    lname.met_quota_prefix + "5": CWLocationData(rname.hub, 104, "Quotas"),

    # ==================== VIEW MILESTONES ====================
    lname.reached_1k:   CWLocationData(rname.hub, 200, "Views"),
    lname.reached_2k:   CWLocationData(rname.hub, 201, "Views"),
    lname.reached_3k:   CWLocationData(rname.hub, 202, "Views"),
    lname.reached_13k:  CWLocationData(rname.hub, 203, "Views"),
    lname.reached_26k:  CWLocationData(rname.hub, 204, "Views"),
    lname.reached_39k:  CWLocationData(rname.hub, 205, "Views"),
    lname.reached_43k:  CWLocationData(rname.hub, 206, "Views"),
    lname.reached_85k:  CWLocationData(rname.hub, 207, "Views"),
    lname.reached_128k: CWLocationData(rname.hub, 208, "Views"),
    lname.reached_150k: CWLocationData(rname.hub, 209, "Views"),
    lname.reached_220k: CWLocationData(rname.hub, 210, "Views"),
    lname.reached_325k: CWLocationData(rname.hub, 211, "Views"),
    lname.reached_375k: CWLocationData(rname.hub, 212, "Views"),
    lname.reached_430k: CWLocationData(rname.hub, 213, "Views"),
    lname.reached_645k: CWLocationData(rname.hub, 214, "Views"),

    # ==================== MONSTER FILMING CHECKS ====================
    "Filmed Slurper":       CWLocationData(rname.dungeon, 300, "Monsters"),
    "Filmed Zombe":         CWLocationData(rname.dungeon, 301, "Monsters"),
    "Filmed Worm":          CWLocationData(rname.dungeon, 302, "Monsters"),
    "Filmed Mouthe":        CWLocationData(rname.dungeon, 303, "Monsters"),
    "Filmed Flicker":       CWLocationData(rname.dungeon, 304, "Monsters"),
    "Filmed Cam Creep":     CWLocationData(rname.dungeon, 305, "Monsters"),
    "Filmed Infiltrator":   CWLocationData(rname.dungeon, 306, "Monsters"),
    "Filmed Button Robot":  CWLocationData(rname.dungeon, 307, "Monsters"),
    "Filmed Puffo":         CWLocationData(rname.dungeon, 308, "Monsters"),
    "Filmed Black Hole Bot":CWLocationData(rname.dungeon, 309, "Monsters"),
    "Filmed Snatcho":       CWLocationData(rname.dungeon, 310, "Monsters"),
    "Filmed Whisk":         CWLocationData(rname.dungeon, 311, "Monsters"),
    "Filmed Spider":        CWLocationData(rname.dungeon, 312, "Monsters"),
    "Filmed Ear":           CWLocationData(rname.dungeon, 313, "Monsters"),
    "Filmed Jelly":         CWLocationData(rname.dungeon, 314, "Monsters"),
    "Filmed Weeping":       CWLocationData(rname.dungeon, 315, "Monsters"),
    "Filmed Bomber":        CWLocationData(rname.dungeon, 316, "Monsters"),
    "Filmed Dog":           CWLocationData(rname.dungeon, 317, "Monsters"),  # Robot Dog
    "Filmed Eye Guy":       CWLocationData(rname.dungeon, 318, "Monsters"),
    "Filmed Fire":          CWLocationData(rname.dungeon, 319, "Monsters"),
    "Filmed Knifo":         CWLocationData(rname.dungeon, 320, "Monsters"),
    "Filmed Larva":         CWLocationData(rname.dungeon, 321, "Monsters"),
    "Filmed Arms":          CWLocationData(rname.dungeon, 322, "Monsters"),
    "Filmed Harpooner":     CWLocationData(rname.dungeon, 323, "Monsters"),
    "Filmed Mime":          CWLocationData(rname.dungeon, 324, "Monsters"),
    "Filmed Barnacle Ball": CWLocationData(rname.dungeon, 325, "Monsters"),
    "Filmed Snail Spawner": CWLocationData(rname.dungeon, 326, "Monsters"),
    "Filmed Big Slap":      CWLocationData(rname.dungeon, 327, "Monsters"),
    "Filmed Streamer":      CWLocationData(rname.dungeon, 328, "Monsters"),
    "Filmed Ultra Knifo":   CWLocationData(rname.dungeon, 329, "Monsters"),
    "Filmed Angler":        CWLocationData(rname.dungeon, 330, "Monsters"),
    "Filmed Iron Maiden":   CWLocationData(rname.dungeon, 331, "Monsters"),
    "Filmed Grabber Snake": CWLocationData(rname.dungeon, 332, "Monsters"),

    # ==================== ARTIFACT FILMING CHECKS ====================
    "Filmed Ribcage":             CWLocationData(rname.dungeon, 400, "Artifacts"),
    "Filmed Skull":               CWLocationData(rname.dungeon, 401, "Artifacts"),
    "Filmed Spine":               CWLocationData(rname.dungeon, 402, "Artifacts"),
    "Filmed Bone":                CWLocationData(rname.dungeon, 403, "Artifacts"),
    "Filmed Brain on a Stick":    CWLocationData(rname.dungeon, 404, "Artifacts"),
    "Filmed Radio":               CWLocationData(rname.dungeon, 405, "Artifacts"),
    "Filmed Shroom":              CWLocationData(rname.dungeon, 406, "Artifacts"),
    "Filmed Animal Statues":      CWLocationData(rname.dungeon, 407, "Artifacts"),
    "Filmed Radioactive Container": CWLocationData(rname.dungeon, 408, "Artifacts"),
    "Filmed Old Painting":        CWLocationData(rname.dungeon, 409, "Artifacts"),
    "Filmed Chorby":              CWLocationData(rname.dungeon, 410, "Artifacts"),
    "Filmed Apple":               CWLocationData(rname.dungeon, 411, "Artifacts"),

    # ==================== STORE PURCHASE CHECKS ====================
    "Bought Old Flashlight":       CWLocationData(rname.hub, 500, "Store Purchases"),
    "Bought Flare":                CWLocationData(rname.hub, 501, "Store Purchases"),
    "Bought Modern Flashlight":    CWLocationData(rname.hub, 502, "Store Purchases"),
    "Bought Long Flashlight":      CWLocationData(rname.hub, 503, "Store Purchases"),
    "Bought Modern Flashlight Pro":CWLocationData(rname.hub, 504, "Store Purchases"),
    "Bought Long Flashlight Pro":  CWLocationData(rname.hub, 505, "Store Purchases"),
    "Bought Hugger":               CWLocationData(rname.hub, 506, "Store Purchases"),
    "Bought Defibrillator":        CWLocationData(rname.hub, 507, "Store Purchases"),
    "Bought Reporter Mic":         CWLocationData(rname.hub, 508, "Store Purchases"),
    "Bought Boom Mic":             CWLocationData(rname.hub, 509, "Store Purchases"),
    "Bought Clapper":              CWLocationData(rname.hub, 510, "Store Purchases"),
    "Bought Sound Player":         CWLocationData(rname.hub, 511, "Store Purchases"),
    "Bought Goo Ball":             CWLocationData(rname.hub, 512, "Store Purchases"),
    "Bought Rescue Hook":          CWLocationData(rname.hub, 513, "Store Purchases"),
    "Bought Shock Stick":          CWLocationData(rname.hub, 514, "Store Purchases"),

    # ==================== EMOTE CHECKS ====================
    "Bought Applause":           CWLocationData(rname.hub, 550, "Emotes"),
    "Bought Workout 1":          CWLocationData(rname.hub, 551, "Emotes"),
    "Bought Confused":           CWLocationData(rname.hub, 552, "Emotes"),
    "Bought Dance 103":          CWLocationData(rname.hub, 553, "Emotes"),
    "Bought Dance 102":          CWLocationData(rname.hub, 554, "Emotes"),
    "Bought Dance 101":          CWLocationData(rname.hub, 555, "Emotes"),
    "Bought Backflip":           CWLocationData(rname.hub, 556, "Emotes"),
    "Bought Gymnastics":         CWLocationData(rname.hub, 557, "Emotes"),
    "Bought Caring":             CWLocationData(rname.hub, 558, "Emotes"),
    "Bought Ancient Gestures 3": CWLocationData(rname.hub, 559, "Emotes"),
    "Bought Ancient Gestures 2": CWLocationData(rname.hub, 560, "Emotes"),
    "Bought Yoga":               CWLocationData(rname.hub, 561, "Emotes"),
    "Bought Workout 2":          CWLocationData(rname.hub, 562, "Emotes"),
    "Bought Thumbnail 1":        CWLocationData(rname.hub, 563, "Emotes"),
    "Bought Thumbnail 2":        CWLocationData(rname.hub, 564, "Emotes"),
    "Bought Ancient Gestures 1": CWLocationData(rname.hub, 565, "Emotes"),

    # ==================== MISC ====================
    "Bought Party Popper": CWLocationData(rname.hub, 570, "Store Purchases"),

    # ==================== HAT CHECKS ====================
    "Bought Balaclava":    CWLocationData(rname.hub, 600, "Hats"),
    "Bought Beanie":       CWLocationData(rname.hub, 601, "Hats"),
    "Bought Bucket Hat":   CWLocationData(rname.hub, 602, "Hats"),
    "Bought Cat Ears":     CWLocationData(rname.hub, 603, "Hats"),
    "Bought Chefs Hat":    CWLocationData(rname.hub, 604, "Hats"),
    "Bought Floppy Hat":   CWLocationData(rname.hub, 605, "Hats"),
    "Bought Homburg":      CWLocationData(rname.hub, 606, "Hats"),
    "Bought Curly Hair":   CWLocationData(rname.hub, 607, "Hats"),
    "Bought Bowler Hat":   CWLocationData(rname.hub, 608, "Hats"),
    "Bought Cap":          CWLocationData(rname.hub, 609, "Hats"),
    "Bought Propeller Hat":CWLocationData(rname.hub, 610, "Hats"),
    "Bought Clown Hair":   CWLocationData(rname.hub, 611, "Hats"),
    "Bought Cowboy Hat":   CWLocationData(rname.hub, 612, "Hats"),
    "Bought Crown":        CWLocationData(rname.hub, 613, "Hats"),
    "Bought Halo":         CWLocationData(rname.hub, 614, "Hats"),
    "Bought Horns":        CWLocationData(rname.hub, 615, "Hats"),
    "Bought Hotdog Hat":   CWLocationData(rname.hub, 616, "Hats"),
    "Bought Jesters Hat":  CWLocationData(rname.hub, 617, "Hats"),
    "Bought Ghost Hat":    CWLocationData(rname.hub, 618, "Hats"),
    "Bought Milk Hat":     CWLocationData(rname.hub, 619, "Hats"),
    "Bought News Cap":     CWLocationData(rname.hub, 620, "Hats"),
    "Bought Pirate Hat":   CWLocationData(rname.hub, 621, "Hats"),
    "Bought Sports Helmet":CWLocationData(rname.hub, 622, "Hats"),
    "Bought Tooop Hat":    CWLocationData(rname.hub, 623, "Hats"),
    "Bought Top Hat":      CWLocationData(rname.hub, 624, "Hats"),
    "Bought Party Hat":    CWLocationData(rname.hub, 625, "Hats"),
    "Bought Shroom Hat":   CWLocationData(rname.hub, 626, "Hats"),
    "Bought Ushanka":      CWLocationData(rname.hub, 627, "Hats"),
    "Bought Witch Hat":    CWLocationData(rname.hub, 628, "Hats"),
    "Bought Hard Hat":     CWLocationData(rname.hub, 629, "Hats"),
    "Bought Savannah Hair":CWLocationData(rname.hub, 630, "Hats"),

    # ==================== SPONSORSHIP CHECKS ====================
    "Accepted a Sponsorship": CWLocationData(rname.hub, 700, "Sponsorships"),
    "Completed Sponsorship 1":CWLocationData(rname.hub, 701, "Sponsorships"),
    "Completed Sponsorship 2":CWLocationData(rname.hub, 702, "Sponsorships"),
    "Completed Sponsorship 3":CWLocationData(rname.hub, 703, "Sponsorships"),

    # ==================== VICTORY (EVENT) ====================
    lname.victory: CWLocationData(rname.hub, None, "Event"),
}

# ==================== COMPUTED LOOKUPS ====================
location_name_to_id: Dict[str, Optional[int]] = {}

for _loc_name, _loc_data in location_table.items():
    if _loc_data.location_id_offset is not None:
        location_name_to_id[_loc_name] = location_base_id + _loc_data.location_id_offset
    else:
        location_name_to_id[_loc_name] = None


def _get_location_group(loc_name: str) -> str:
    return location_table[loc_name].location_group or ""


event_locations: List[str] = [
    name for name, data in location_table.items()
    if data.location_group == "Event"
]

# Count real (non-event) locations for pool balancing; adjusted downward in __init__.py
# when optional location groups are disabled by player options.
location_total: int = sum(
    1 for data in location_table.values()
    if data.location_id_offset is not None
)

# ==================== LOCATION NAME GROUPS ====================
_artifact_keywords = {
    "Ribcage", "Skull", "Spine", "Bone", "Brain",
    "Radio", "Shroom", "Animal", "Radioactive", "Painting", "Chorby", "Apple"
}

location_name_groups: Dict[str, Set[str]] = {
    "Days": {
        lname.extracted_footage_prefix + str(i) for i in range(1, 16)
    },
    "Quotas": {
        lname.met_quota_prefix + str(i) for i in range(1, 6)
    },
    "Views": {
        name for name in location_table if location_table[name].location_group == "Views"
    },
    "Monsters": {
        name for name in location_table if location_table[name].location_group == "Monsters"
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
}
