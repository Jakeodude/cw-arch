# worlds/content_warning/items.py

from BaseClasses import Item, ItemClassification

class ContentWarningItem(Item):
    game = "Content Warning"

# Base ID - must match the one in locations.py (or be consistent across files)
base_id = 98765000

# ==================== ITEM TABLE ====================
# Keys are the exact item names that will appear in the randomizer / client
item_table = {
    # ------------------- Progression / Useful Items -------------------
    "Camera Upgrade": base_id + 0,          # Better recording time / quality
    "Advanced Camera": base_id + 1,         # Night vision + longer record
    "Parabolic Mic": base_id + 2,           # Better monster audio capture
    "Rescue Hook": base_id + 3,             # Pulling tool for rescues
    "Shock Stick": base_id + 4,             # Stun tool (safety + comedy)
    "Goo Ball Pack": base_id + 5,           # Traps for monsters
    "Defibrillator": base_id + 6,           # Revive tool

    # Health & Oxygen Progression
    "Increased Health": base_id + 20,       # +Health pool
    "Health Upgrade": base_id + 21,
    "Increased Oxygen": base_id + 22,       # Larger oxygen tank
    "Oxygen Tank Upgrade": base_id + 23,
    "Extra Oxygen": base_id + 24,

    # Money ($ in-game currency) - helps buy store items faster
    "Money Boost": base_id + 40,
    "Big Money Boost": base_id + 41,
    "Extra Cash": base_id + 42,
    "$500": base_id + 43,
    "$2000": base_id + 44,

    # Meta Coins (permanent currency) - unlocks hats & island upgrades
    "Meta Coin": base_id + 60,
    "Meta Coin Pack": base_id + 61,
    "Big Meta Coin Pack": base_id + 62,

    # View / Content Boosts (helps hit view milestones & quotas)
    "View Boost": base_id + 80,
    "Big View Boost": base_id + 81,
    "Viral Moment": base_id + 82,

    # ------------------- Filler / Trap Items -------------------
    "Nothing": base_id + 100,               # True junk
    "Extra Views": base_id + 101,
    "Small Cash": base_id + 102,
    "Minor Health Pack": base_id + 103,
    "Minor Oxygen": base_id + 104,
    "Monster Repellent": base_id + 105,     # Temporary safety

    # Traps (fun chaos)
    "Camera Malfunction": base_id + 120,
    "Monster Swarm": base_id + 121,
    "Oxygen Leak": base_id + 122,
    "Low Battery": base_id + 123,

    # ------------------- Victory Item -------------------
    "Viral Sensation": base_id + 200,       # Goal item - reach high views / film everything
}

# Classification helper (used in create_item)
def get_item_classification(name: str) -> ItemClassification:
    if name in {"Camera Upgrade", "Advanced Camera", "Parabolic Mic", "Rescue Hook",
                "Shock Stick", "Defibrillator", "Increased Health", "Health Upgrade",
                "Increased Oxygen", "Oxygen Tank Upgrade", "Viral Sensation"}:
        return ItemClassification.progression
    elif name in {"Money Boost", "Big Money Boost", "$2000", "Meta Coin Pack",
                  "Big Meta Coin Pack", "View Boost", "Big View Boost", "Viral Moment"}:
        return ItemClassification.progression_skip_balancing  # useful but not strictly required
    elif "Trap" in name or name in {"Camera Malfunction", "Monster Swarm", "Oxygen Leak", "Low Battery"}:
        return ItemClassification.trap
    else:
        return ItemClassification.filler


# Optional: Item groups for logic / hints
item_name_groups = {
    "Progression": {"Camera Upgrade", "Advanced Camera", "Parabolic Mic", "Rescue Hook",
                    "Shock Stick", "Defibrillator", "Increased Health", "Increased Oxygen"},
    "Money": {"Money Boost", "Big Money Boost", "Extra Cash", "$500", "$2000"},
    "Meta Coins": {"Meta Coin", "Meta Coin Pack", "Big Meta Coin Pack"},
    "Health": {"Increased Health", "Health Upgrade", "Minor Health Pack"},
    "Oxygen": {"Increased Oxygen", "Oxygen Tank Upgrade", "Extra Oxygen", "Minor Oxygen"},
    "Views": {"View Boost", "Big View Boost", "Viral Moment"},
    "Traps": {"Camera Malfunction", "Monster Swarm", "Oxygen Leak", "Low Battery"},
}