# worlds/content_warning/logic.py
# Helper state-check functions used by rules.py

from typing import TYPE_CHECKING, List
from BaseClasses import CollectionState

from .names import item_names as iname

if TYPE_CHECKING:
    from . import ContentWarningWorld


# ---------------------------------------------------------------------------
# Camera & Exploration
# ---------------------------------------------------------------------------

def can_enter_dungeon(state: CollectionState, player: int) -> bool:
    """Player has at least one Progressive Camera upgrade — ready to film."""
    return state.count(iname.prog_camera, player) >= 1


def can_explore_mid_dungeon(state: CollectionState, player: int) -> bool:
    """Player has enough oxygen to search deeper parts of The Old World."""
    return state.count(iname.prog_oxygen, player) >= 1


def can_explore_late_dungeon(state: CollectionState, player: int) -> bool:
    """Player has the oxygen and camera upgrades for the deepest sections."""
    return (
        state.count(iname.prog_oxygen, player) >= 2
        and state.count(iname.prog_camera, player) >= 1
    )


# ---------------------------------------------------------------------------
# Progressive Views (gates view milestone checks)
# ---------------------------------------------------------------------------

def view_boost_count(state: CollectionState, player: int) -> int:
    """Returns the number of Progressive Views items the player has collected.
    Each copy multiplies video view income by 1.1×."""
    return state.count(iname.prog_views, player)


def has_views(state: CollectionState, player: int, required: int) -> bool:
    """True if the player has at least *required* Progressive Views items."""
    return view_boost_count(state, player) >= required


# ---------------------------------------------------------------------------
# Counting reachable locations (used for goal/sanity rules)
# ---------------------------------------------------------------------------

def count_reachable(state: CollectionState, player: int, locations: List[str]) -> int:
    """Return how many of the given location names are currently reachable."""
    return sum(1 for loc in locations if state.can_reach_location(loc, player))
