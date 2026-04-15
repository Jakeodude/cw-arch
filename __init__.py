# worlds/content_warning/__init__.py

import math
from typing import Dict, List, Any

from worlds.AutoWorld import WebWorld, World
from BaseClasses import Region, ItemClassification

from .items import (
    item_table, item_name_to_id, item_name_groups,
    filler_items, trap_items,
    ContentWarningItem, CWItemData,
)
from .locations import (
    location_table, location_name_to_id, location_name_groups, location_total,
    ContentWarningLocation,
)
from .regions import CW_regions
from .rules import set_region_rules, set_location_rules
from .options import ContentWarningGameOptions
from .names import item_names as iname, location_names as lname, region_names as rname


class ContentWarningWebWorld(WebWorld):
    theme: str = "dirt"
    game: str = "Content Warning"


class ContentWarningWorld(World):
    """
    Content Warning is a co-op horror game in which you and your crew descend
    into an abandoned underground facility, film monsters for views, and try
    to go viral before your quota runs out.
    """

    game: str = "Content Warning"
    web = ContentWarningWebWorld()

    options_dataclass = ContentWarningGameOptions
    options: ContentWarningGameOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    # Mutable per-instance location count (adjusted for disabled option groups)
    location_total: int = location_total

    # -----------------------------------------------------------------------
    # Item helpers
    # -----------------------------------------------------------------------

    def create_item(self, name: str) -> ContentWarningItem:
        data: CWItemData = item_table[name]
        item_id = item_name_to_id[name]  # None for events
        return ContentWarningItem(name, data.classification, item_id, self.player)

    def create_event(self, name: str) -> ContentWarningItem:
        return ContentWarningItem(
            name, ItemClassification.progression, None, self.player
        )

    def get_filler_item_name(self) -> str:
        """Return a random filler item name (used by AP when it needs padding)."""
        return self.random.choice(filler_items)

    # -----------------------------------------------------------------------
    # Item pool
    # -----------------------------------------------------------------------

    def create_items(self) -> None:
        cw_items: List[ContentWarningItem] = []
        items_to_create: Dict[str, int] = {
            name: data.quantity_in_item_pool
            for name, data in item_table.items()
            if data.item_group != "Event"    # events are placed separately
        }

        # ------------------------------------------------------------------
        # Adjust location_total based on which optional groups are enabled.
        # We do this here (before pool math) so filler calculation is correct.
        # ------------------------------------------------------------------
        self.location_total = location_total  # reset to base each generation

        optional_groups = {
            "Hats":         self.options.include_hats.value,
            "Emotes":       self.options.include_emotes.value,
            "Sponsorships": self.options.include_sponsorships.value,
        }
        for group, enabled in optional_groups.items():
            if not enabled:
                removed = sum(
                    1 for data in location_table.values()
                    if data.location_group == group
                )
                self.location_total -= removed

        # ------------------------------------------------------------------
        # Victory event — placed manually in create_regions()
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # Calculate how much filler is needed to fill remaining slots.
        # ------------------------------------------------------------------
        named_total: int = sum(items_to_create.values())
        total_filler = self.location_total - named_total

        if total_filler < 0:
            total_filler = 0

        # Randomly pick from filler items to pad the pool.
        for _ in range(total_filler):
            cw_items.append(self.create_item(self.random.choice(filler_items)))

        # Add all named (non-filler-pad) items.
        for name, quantity in items_to_create.items():
            for _ in range(quantity):
                cw_items.append(self.create_item(name))

        self.multiworld.itempool += cw_items

    # -----------------------------------------------------------------------
    # Regions & Locations
    # -----------------------------------------------------------------------

    def create_regions(self) -> None:
        # Create all regions.
        for region_name in CW_regions:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Wire up exits.
        for region_name, exits in CW_regions.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(exits)

        # Place each location into its designated region, respecting options.
        disabled_groups = set()
        if not self.options.include_hats.value:
            disabled_groups.add("Hats")
        if not self.options.include_emotes.value:
            disabled_groups.add("Emotes")
        if not self.options.include_sponsorships.value:
            disabled_groups.add("Sponsorships")

        for loc_name, loc_data in location_table.items():
            # Skip event locations (handled below) and disabled groups.
            if loc_data.location_group == "Event":
                continue
            if loc_data.location_group in disabled_groups:
                continue

            region = self.multiworld.get_region(loc_data.region, self.player)
            loc_id = location_name_to_id[loc_name]
            location = ContentWarningLocation(
                self.player, loc_name, loc_id, region
            )
            region.locations.append(location)

        # Place the Victory event location + item in the Hub.
        hub = self.multiworld.get_region(rname.hub, self.player)
        victory_loc = ContentWarningLocation(
            self.player, lname.victory, None, hub
        )
        victory_loc.place_locked_item(
            ContentWarningItem(
                lname.victory, ItemClassification.progression, None, self.player
            )
        )
        hub.locations.append(victory_loc)

    # -----------------------------------------------------------------------
    # Rules
    # -----------------------------------------------------------------------

    def set_rules(self) -> None:
        set_region_rules(self)
        set_location_rules(self)

    # -----------------------------------------------------------------------
    # Slot data (sent to the game client)
    # -----------------------------------------------------------------------

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal":                  int(self.options.goal.value),
            "include_hats":          bool(self.options.include_hats.value),
            "include_emotes":        bool(self.options.include_emotes.value),
            "include_sponsorships":  bool(self.options.include_sponsorships.value),
            "dungeon_logic":         int(self.options.dungeon_logic.value),
        }
