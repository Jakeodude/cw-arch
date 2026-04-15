# worlds/content_warning/regions.py

from typing import Dict, Set

from .names import region_names as rname

# Directed graph of region → set of exit region names.
# Menu  ──► Hub  ──► Dungeon
# Access rules for the Hub→Dungeon entrance are set in rules.py.
CW_regions: Dict[str, Set[str]] = {
    rname.menu:    {rname.hub},
    rname.hub:     {rname.dungeon},
    rname.dungeon: set(),
}
