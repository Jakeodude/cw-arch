# worlds/content_warning/rules.py

from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, set_rule
from BaseClasses import CollectionState, ItemClassification

from .names import item_names as iname
from .names import location_names as lname
from .names import region_names as rname
from .locations import location_table
from . import logic

if TYPE_CHECKING:
    from . import ContentWarningWorld


# ---------------------------------------------------------------------------
# Monsters that are considered dangerous enough to require safety gear
# (on Easy logic).  Anything not listed here is accessible by default.
# ---------------------------------------------------------------------------
_DANGEROUS_MONSTERS = {
    "Filmed Knifo",
    "Filmed Ultra Knifo",
    "Filmed Harpooner",
    "Filmed Iron Maiden",
    "Filmed Grabber Snake",
    "Filmed Big Slap",
    "Filmed Black Hole Bot",
    "Filmed Streamer",
    "Filmed Angler",
    "Filmed Bomber",
    "Filmed Fire",
}

# Monsters that additionally require full survival gear (safety + health + oxygen).
_VERY_DANGEROUS_MONSTERS = {
    "Filmed Ultra Knifo",
    "Filmed Iron Maiden",
    "Filmed Grabber Snake",
    "Filmed Angler",
}

# ---------------------------------------------------------------------------
# View milestone → minimum view_boost_count threshold
# ---------------------------------------------------------------------------
_VIEW_THRESHOLDS = {
    lname.reached_85k:  1,
    lname.reached_128k: 1,
    lname.reached_150k: 2,
    lname.reached_220k: 2,
    lname.reached_325k: 3,
    lname.reached_375k: 3,
    lname.reached_430k: 4,
    lname.reached_645k: 5,
}


def set_region_rules(world: "ContentWarningWorld") -> None:
    """Set entrance access rules between regions."""
    multiworld = world.multiworld
    player = world.player

    # Hub is always accessible from Menu — no rule needed.

    # Dungeon requires at least the camera upgrade to enter (you need equipment
    # to have a reason to go down; matches the game's progression feel).
    multiworld.get_entrance(
        f"{rname.hub} -> {rname.dungeon}", player
    ).access_rule = lambda state: state.has(iname.camera_upgrade, player)


def set_location_rules(world: "ContentWarningWorld") -> None:
    """Set individual location access rules and the completion condition."""
    multiworld = world.multiworld
    player = world.player
    options = world.options
    easy_logic = (options.dungeon_logic.value == options.dungeon_logic.option_easy)

    # ---- Completion condition ----
    multiworld.completion_condition[player] = lambda state: state.has(
        lname.victory, player
    )

    # ---- Victory location rules ----
    # Viral Sensation goal: reach the top view milestone.
    if options.goal.value == options.goal.option_viral_sensation:
        add_rule(
            multiworld.get_location(lname.victory, player),
            lambda state: logic.has_views(state, player, 5)
        )

    # Content Complete goal: film every monster and artifact.
    elif options.goal.value == options.goal.option_content_complete:
        for loc_name, loc_data in location_table.items():
            if loc_data.location_group in ("Monsters", "Artifacts"):
                add_rule(
                    multiworld.get_location(lname.victory, player),
                    lambda state, ln=loc_name: state.can_reach_location(ln, player)
                )

    # ---- View milestone rules ----
    for milestone, threshold in _VIEW_THRESHOLDS.items():
        add_rule(
            multiworld.get_location(milestone, player),
            lambda state, t=threshold: logic.has_views(state, player, t)
        )

    # ---- Monster filming rules (Easy logic only) ----
    if easy_logic:
        for monster in _DANGEROUS_MONSTERS:
            if monster in _VERY_DANGEROUS_MONSTERS:
                add_rule(
                    multiworld.get_location(monster, player),
                    lambda state: logic.can_survive_dungeon(state, player)
                )
            else:
                add_rule(
                    multiworld.get_location(monster, player),
                    lambda state: logic.has_safety_gear(state, player)
                )

    # ---- Quota rules: each quota requires the previous one be reachable ----
    for i in range(2, 6):
        prev = lname.met_quota_prefix + str(i - 1)
        curr = lname.met_quota_prefix + str(i)
        add_rule(
            multiworld.get_location(curr, player),
            lambda state, p=prev: state.can_reach_location(p, player)
        )

    # ---- Day extraction rules: each day requires the previous ----
    for i in range(2, 16):
        prev = lname.extracted_footage_prefix + str(i - 1)
        curr = lname.extracted_footage_prefix + str(i)
        add_rule(
            multiworld.get_location(curr, player),
            lambda state, p=prev: state.can_reach_location(p, player)
        )
