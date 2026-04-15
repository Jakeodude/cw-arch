# worlds/content_warning/logic.py
# Helper state-check functions used by rules.py

from typing import TYPE_CHECKING
from BaseClasses import CollectionState

from .names import item_names as iname

if TYPE_CHECKING:
    from . import ContentWarningWorld


def has_safety_gear(state: CollectionState, player: int) -> bool:
    """Player has at least one piece of survival/safety equipment."""
    return state.has_any(
        {iname.shock_stick, iname.rescue_hook, iname.defibrillator},
        player
    )


def has_health_buffer(state: CollectionState, player: int) -> bool:
    """Player has extra health to survive deep-dungeon encounters."""
    return state.has_any({iname.increased_health, iname.health_upgrade}, player)


def has_oxygen_buffer(state: CollectionState, player: int) -> bool:
    """Player has enough oxygen to explore longer without surfacing."""
    return state.has_any({iname.increased_oxygen, iname.oxygen_tank_upgrade}, player)


def can_survive_dungeon(state: CollectionState, player: int) -> bool:
    """Full survival kit for dangerous deep-dungeon encounters."""
    return (
        has_safety_gear(state, player)
        and has_health_buffer(state, player)
        and has_oxygen_buffer(state, player)
    )


def view_boost_count(state: CollectionState, player: int) -> int:
    """Returns a weighted count of view-boosting items the player has received.
    Big View Boost counts as 2 units; View Boost counts as 1."""
    count = state.count(iname.view_boost, player)
    count += state.count(iname.big_view_boost, player) * 2
    return count


def has_views(state: CollectionState, player: int, required: int) -> bool:
    """True if the player's accumulated view boosts meet the required threshold."""
    return view_boost_count(state, player) >= required
