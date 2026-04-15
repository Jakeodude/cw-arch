# worlds/content_warning/locations.py

from .Sample import options  # optional, if you want to reference options later

# Base ID - choose a high unique number so it doesn't conflict with other worlds
base_id = 98765000

location_table = {
    # ==================== BASIC EXTRACTION & DAY CHECKS ====================
    "Any Extraction": base_id + 0,  # Any successful film extraction + upload

    "Extracted Footage on Day 1": base_id + 1,
    "Extracted Footage on Day 2": base_id + 2,
    "Extracted Footage on Day 3": base_id + 3,
    "Extracted Footage on Day 4": base_id + 4,
    "Extracted Footage on Day 5": base_id + 5,
    "Extracted Footage on Day 6": base_id + 6,
    "Extracted Footage on Day 7": base_id + 7,
    "Extracted Footage on Day 8": base_id + 8,
    "Extracted Footage on Day 9": base_id + 9,
    "Extracted Footage on Day 10": base_id + 10,
    "Extracted Footage on Day 11": base_id + 11,
    "Extracted Footage on Day 12": base_id + 12,
    "Extracted Footage on Day 13": base_id + 13,
    "Extracted Footage on Day 14": base_id + 14,
    "Extracted Footage on Day 15": base_id + 15,
    

    # ==================== QUOTA CHECKS ====================
    "Met Quota 1": base_id + 100,
    "Met Quota 2": base_id + 101,
    "Met Quota 3": base_id + 102,
    "Met Quota 4": base_id + 103,
    "Met Quota 5": base_id + 104,

    # ==================== VIEWS MILESTONES (your exact list) ====================
    "Reached 1,000 Total Views": base_id + 200,
    "Reached 2,000 Total Views": base_id + 201,
    "Reached 3,000 Total Views": base_id + 202,
    "Reached 13,000 Total Views": base_id + 203,
    "Reached 26,000 Total Views": base_id + 204,
    "Reached 39,000 Total Views": base_id + 205,
    "Reached 43,000 Total Views": base_id + 206,
    "Reached 85,000 Total Views": base_id + 207,
    "Reached 128,000 Total Views": base_id + 208,
    "Reached 150,000 Total Views": base_id + 209,
    "Reached 220,000 Total Views": base_id + 210,
    "Reached 325,000 Total Views": base_id + 211,
    "Reached 375,000 Total Views": base_id + 212,
    "Reached 430,000 Total Views": base_id + 213,
    "Reached 645,000 Total Views": base_id + 214,

    # ==================== MONSTER FILMING CHECKS (32) ====================
    "Filmed Slurper": base_id + 300,
    "Filmed Zombe": base_id + 301,          # Snail Man
    "Filmed Worm": base_id + 302,
    "Filmed Mouthe": base_id + 303,
    "Filmed Flicker": base_id + 304,
    "Filmed Cam Creep": base_id + 305,
    "Filmed Infiltrator": base_id + 306,
    "Filmed Button Robot": base_id + 307,
    "Filmed Puffo": base_id + 308,
    "Filmed Black Hole Bot": base_id + 309,
    "Filmed Snatcho": base_id + 310,
    "Filmed Whisk": base_id + 311,
    "Filmed Spider": base_id + 312,
    "Filmed Ear": base_id + 313,
    "Filmed Jelly": base_id + 314,
    "Filmed Weeping": base_id + 315,
    "Filmed Bomber": base_id + 316,
    "Filmed Dog": base_id + 317,            # Robot Dog
    "Filmed Eye Guy": base_id + 318,
    "Filmed Fire": base_id + 319,
    "Filmed Knifo": base_id + 320,
    "Filmed Larva": base_id + 321,
    "Filmed Arms": base_id + 322,
    "Filmed Harpooner": base_id + 323,
    "Filmed Mime": base_id + 324,
    "Filmed Barnacle Ball": base_id + 325,
    "Filmed Snail Spawner": base_id + 326,
    "Filmed Big Slap": base_id + 327,
    "Filmed Streamer": base_id + 328,
    "Filmed Ultra Knifo": base_id + 329,
    "Filmed Angler": base_id + 330,
    "Filmed Iron Maiden": base_id + 331,
    "Filmed Grabber Snake": base_id + 332,   # extra for completeness if needed, adjust if over 32

    # ==================== ARTIFACT FILMING CHECKS (12) ====================
    "Filmed Ribcage": base_id + 400,
    "Filmed Skull": base_id + 401,
    "Filmed Spine": base_id + 402,
    "Filmed Bone": base_id + 403,
    "Filmed Brain on a Stick": base_id + 404,
    "Filmed Radio": base_id + 405,
    "Filmed Shroom": base_id + 406,
    "Filmed Animal Statues": base_id + 407,
    "Filmed Radioactive Container": base_id + 408,
    "Filmed Old Painting": base_id + 409,
    "Filmed Chorby": base_id + 410,
    "Filmed Apple": base_id + 411,

    # ==================== PURCHASE CHECKS - STORE ITEMS (15) ====================
    "Bought Old Flashlight": base_id + 500,
    "Bought Flare": base_id + 501,
    "Bought Modern Flashlight": base_id + 502,
    "Bought Long Flashlight": base_id + 503,
    "Bought Modern Flashlight Pro": base_id + 504,
    "Bought Long Flashlight Pro": base_id + 505,
    "Bought Hugger": base_id + 506,
    "Bought Defibrillator": base_id + 507,
    "Bought Reporter Mic": base_id + 508,
    "Bought Boom Mic": base_id + 509,
    "Bought Clapper": base_id + 510,
    "Bought Sound Player": base_id + 511,
    "Bought Goo Ball": base_id + 512,
    "Bought Rescue Hook": base_id + 513,
    "Bought Shock Stick": base_id + 514,

    # ==================== EMOTES (16) ====================
    "Bought Applause": base_id + 550,
    "Bought Workout 1": base_id + 551,
    "Bought Confused": base_id + 552,
    "Bought Dance 103": base_id + 553,
    "Bought Dance 102": base_id + 554,
    "Bought Dance 101": base_id + 555,
    "Bought Backflip": base_id + 556,
    "Bought Gymnastics": base_id + 557,
    "Bought Caring": base_id + 558,
    "Bought Ancient Gestures 3": base_id + 559,
    "Bought Ancient Gestures 2": base_id + 560,
    "Bought Yoga": base_id + 561,
    "Bought Workout 2": base_id + 562,
    "Bought Thumbnail 1": base_id + 563,
    "Bought Thumbnail 2": base_id + 564,
    "Bought Ancient Gestures 1": base_id + 565,

    # ==================== MISC (1) ====================
    "Bought Party Popper": base_id + 570,

    # ==================== HATS (31) - exact names from Phil's Hat Shop ====================
    "Bought Balaclava": base_id + 600,
    "Bought Beanie": base_id + 601,
    "Bought Bucket Hat": base_id + 602,
    "Bought Cat Ears": base_id + 603,
    "Bought Chefs Hat": base_id + 604,
    "Bought Floppy Hat": base_id + 605,
    "Bought Homburg": base_id + 606,
    "Bought Curly Hair": base_id + 607,
    "Bought Bowler Hat": base_id + 608,
    "Bought Cap": base_id + 609,
    "Bought Propeller Hat": base_id + 610,
    "Bought Clown Hair": base_id + 611,
    "Bought Cowboy Hat": base_id + 612,
    "Bought Crown": base_id + 613,
    "Bought Halo": base_id + 614,
    "Bought Horns": base_id + 615,
    "Bought Hotdog Hat": base_id + 616,
    "Bought Jesters Hat": base_id + 617,
    "Bought Ghost Hat": base_id + 618,
    "Bought Milk Hat": base_id + 619,
    "Bought News Cap": base_id + 620,
    "Bought Pirate Hat": base_id + 621,
    "Bought Sports Helmet": base_id + 622,
    "Bought Tooop Hat": base_id + 623,
    "Bought Top Hat": base_id + 624,
    "Bought Party Hat": base_id + 625,
    "Bought Shroom Hat": base_id + 626,
    "Bought Ushanka": base_id + 627,
    "Bought Witch Hat": base_id + 628,
    "Bought Hard Hat": base_id + 629,
    "Bought Savannah Hair": base_id + 630,   # final one to reach 31

    # ==================== SPONSORSHIP CHECKS (5) ====================
    "Accepted a Sponsorship": base_id + 700,
    "Completed Sponsorship 1": base_id + 701,
    "Completed Sponsorship 2": base_id + 702,
    "Completed Sponsorship 3": base_id + 703,
}

# Optional: location groups for logic / hints / !hint command
location_name_groups = {
    "Days": {f"Extracted Footage on Day {i}" for i in range(1, 21)},
    "Quotas": {f"Met Quota {i}" for i in range(1, 6)},
    "Views": {name for name in location_table if "Total Views" in name},
    "Monsters": {name for name in location_table if name.startswith("Filmed ") and not any(artifact in name for artifact in ["Ribcage", "Skull", "Spine", "Bone", "Brain", "Radio", "Shroom", "Animal", "Radioactive", "Painting", "Chorby", "Apple"])},
    "Artifacts": {name for name in location_table if name.startswith("Filmed ") and any(artifact in name for artifact in ["Ribcage", "Skull", "Spine", "Bone", "Brain", "Radio", "Shroom", "Animal", "Radioactive", "Painting", "Chorby", "Apple"])},
    "Store Purchases": {name for name in location_table if name.startswith("Bought ") and not any(h in name for h in ["Balaclava", "Beanie", "Bucket", "Cat Ears", "Chefs Hat", ...])},  # you can refine
    "Hats": {name for name in location_table if name.startswith("Bought ") and ("Hat" in name or "Hair" in name or "Halo" in name or "Horns" in name or "Crown" in name)},
    "Sponsorships": {"Accepted a Sponsorship", "Completed Sponsorship 1", "Completed Sponsorship 2", "Completed Sponsorship 3"},
}

