# worlds/content_warning/__init__.py

from typing import Dict, List, Any
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Region, ItemClassification, LocationProgressType

from .items import (
    item_table, item_name_to_id, item_name_groups,
    filler_items, trap_items,
    MONEY_FILLER_POOL,
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

# View milestones that should receive filler only when quota_count < 4.
_HIGH_VIEW_MILESTONES = {
    lname.reached_128k,
    lname.reached_150k,
    lname.reached_220k,
    lname.reached_325k,
    lname.reached_375k,
    lname.reached_430k,
    lname.reached_645k,
    lname.reached_850k,
    lname.reached_1m,
}

# Monster locations that require Multiplayer Mode (player_count > 1).
# In solo seeds these locations are skipped entirely in create_regions — the
# player cannot encounter the monster without other players in the lobby, so
# leaving the check in the world (even as filler) would strand any item
# placed there.  Worm was previously here but has been confirmed to spawn
# solo and is now treated as a normal mid-stage monster.
_MULTIPLAYER_ONLY_MONSTERS = {
    "Filmed Weeping",
}

# Tier 2/3 of multiplayer-only monsters inherit the same gate.  Difficult
# monsters (including Weeping) currently have no Monster Tiers entries in
# locations.py, so this set extension is defensive — it ensures the right
# behaviour automatically if tier 2/3 are ever added for these monsters.
_MULTIPLAYER_ONLY_LOCATIONS = (
    set(_MULTIPLAYER_ONLY_MONSTERS)
    | {f"{m} 2" for m in _MULTIPLAYER_ONLY_MONSTERS}
    | {f"{m} 3" for m in _MULTIPLAYER_ONLY_MONSTERS}
)


class ContentWarningWebWorld(WebWorld):
    theme: str = "dirt"
    game: str = "Content Warning"


class ContentWarningWorld(World):
    """
    Content Warning is a co-op horror game in which you and your crew descend
    into an abandoned underground facility (The Old World), film monsters for
    views, and try to go viral before your quota runs out.
    """

    game: str = "Content Warning"
    web = ContentWarningWebWorld()

    options_dataclass = ContentWarningGameOptions
    options: ContentWarningGameOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    # Mutable per-instance location count (recomputed each generation).
    location_total: int = location_total

    # -----------------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------------

    def _compute_reachable_monster_count(self) -> int:
        """Return how many 'Monsters' group locations are logically reachable
        given the current option settings.

        Excludes:
          • Multiplayer-only monsters (Weeping) when multiplayer_mode is off.
          • Difficult-stage monsters when difficult_monsters is off.
        Used by generate_early to clamp monster_hunter_count, and mirrored in
        rules.py when constructing the monster_hunter victory rule.
        """
        options = self.options
        return sum(
            1 for name, data in location_table.items()
            if data.location_group == "Monsters"
            and not (name in _MULTIPLAYER_ONLY_MONSTERS and not options.multiplayer_mode.value)
            and not (data.game_stage == "difficult" and not options.difficult_monsters.value)
        )

    def _compute_location_total(self) -> int:
        """Return the real number of check locations that will be created,
        based on the current option settings."""
        options = self.options
        quota_count = options.quota_count.value if options.quota_requirement.value else 0

        total = 0
        for loc_name, loc_data in location_table.items():
            if loc_data.location_group in (None, "Event"):
                continue
            if loc_data.location_id_offset is None:
                continue

            grp = loc_data.location_group

            # Disabled optional groups
            if grp == "Hats" and not options.include_hats.value:
                continue
            if grp == "Emotes" and not options.include_emotes.value:
                continue
            if grp in ("Sponsorships", "Sponsorsanity") and not options.include_sponsorships.value:
                continue
            if grp == "Sponsorsanity" and not options.sponsorsanity.value:
                continue
            if grp == "Monster Tiers" and not options.monster_tiers.value:
                continue

            # Multiplayer-only checks: skip in solo so the location count
            # matches what create_regions will actually produce.
            if loc_name in _MULTIPLAYER_ONLY_LOCATIONS and not options.multiplayer_mode.value:
                continue

            # Quota locations: only up to quota_count are active
            if grp == "Quotas":
                num = int(loc_name.replace(lname.met_quota_prefix, ""))
                if num > quota_count:
                    continue

            total += 1
        return total

    # -----------------------------------------------------------------------
    # Item helpers
    # -----------------------------------------------------------------------

    def create_item(self, name: str) -> ContentWarningItem:
        data: CWItemData = item_table[name]
        item_id = item_name_to_id[name]
        return ContentWarningItem(name, data.classification, item_id, self.player)

    def create_event(self, name: str) -> ContentWarningItem:
        return ContentWarningItem(
            name, ItemClassification.progression, None, self.player
        )

    def get_filler_item_name(self) -> str:
        """Return a random filler item name (money or meta coins only)."""
        return self.random.choice(filler_items)

    # -----------------------------------------------------------------------
    # Pre-generation validation
    # -----------------------------------------------------------------------

    def generate_early(self) -> None:
        """Clamp option values that depend on runtime-computed reachable counts.

        Runs before create_items and set_rules so the clamped values are used
        consistently throughout generation and reported correctly in fill_slot_data.
        """
        options = self.options

        # Cap monster_hunter_count to the number of monsters actually reachable
        # with the current option set (solo vs multiplayer, difficult vs normal).
        # Without this, a solo seed requesting more monsters than are accessible
        # causes a FillError during generation.
        if "monster_hunter" in options.goal.value:
            max_reachable = self._compute_reachable_monster_count()
            if options.monster_hunter_count.value > max_reachable:
                options.monster_hunter_count.value = max_reachable

    # -----------------------------------------------------------------------
    # Item pool
    # -----------------------------------------------------------------------

    def create_items(self) -> None:
        cw_items: List[ContentWarningItem] = []

        # Recompute active location count for this generation.
        self.location_total = self._compute_location_total()

        # All named (non-event) items go in the pool at their base quantities.
        # Money items have quantity_in_item_pool == 0 and are filled via the
        # weighted filler step below.  Meta coin base quantities are set in
        # items.py to target the early/mid/late budget split.
        items_to_create: Dict[str, int] = {
            name: data.quantity_in_item_pool
            for name, data in item_table.items()
            if data.item_group != "Event"
        }

        named_total: int = sum(items_to_create.values())
        total_filler = max(0, self.location_total - named_total)

        # Remaining slots are filled with weighted money filler.
        # Common: $100 / $200 (3× weight each); Rare: $300 / $400 (1× each).
        for _ in range(total_filler):
            cw_items.append(self.create_item(self.random.choice(MONEY_FILLER_POOL)))

        # Add all named items.
        for name, quantity in items_to_create.items():
            for _ in range(quantity):
                cw_items.append(self.create_item(name))

        self.multiworld.itempool += cw_items

        # -----------------------------------------------------------------------
        # Progression balancing for Meta Coins
        # Push small packages (500 / 1,000) into sphere-1 locations so the
        # early-game budget (~5,000 MC) is accessible before mid/late items
        # unlock.  AP will honour these hints during its fill phase.
        # -----------------------------------------------------------------------
        early_items = self.multiworld.early_items[self.player]
        early_items[iname.meta_coins_500]  = 3   # ≤ 4 in pool → push 3 early
        early_items[iname.meta_coins_1000] = 2   # ≤ 3 in pool → push 2 early

    # -----------------------------------------------------------------------
    # Regions & Locations
    # -----------------------------------------------------------------------

    def create_regions(self) -> None:
        options = self.options
        quota_on    = bool(options.quota_requirement.value)
        quota_count = options.quota_count.value if quota_on else 0
        low_quota   = quota_on and quota_count < 4  # affects high-view milestone logic

        # Build set of disabled location groups.
        disabled_groups: set = set()
        if not options.include_hats.value:
            disabled_groups.add("Hats")
        if not options.include_emotes.value:
            disabled_groups.add("Emotes")
        if not options.include_sponsorships.value:
            disabled_groups.add("Sponsorships")
            disabled_groups.add("Sponsorsanity")
        elif not options.sponsorsanity.value:
            disabled_groups.add("Sponsorsanity")
        if not options.monster_tiers.value:
            disabled_groups.add("Monster Tiers")

        # Create all regions.
        for region_name in CW_regions:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Wire up exits.
        for region_name, exits in CW_regions.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(exits)

        # Place each location into its region.
        for loc_name, loc_data in location_table.items():
            if loc_data.location_group == "Event":
                continue
            if loc_data.location_group in disabled_groups:
                continue

            # Solo seeds: completely omit multiplayer-only checks.  Marking
            # them EXCLUDED would still place a filler item at a location the
            # player can never reach, stranding the item and inflating the
            # location count.
            if loc_name in _MULTIPLAYER_ONLY_LOCATIONS and not options.multiplayer_mode.value:
                continue

            # Variable quota count: skip quotas beyond the configured number.
            if loc_data.location_group == "Quotas":
                if not quota_on:
                    continue
                num = int(loc_name.replace(lname.met_quota_prefix, ""))
                if num > quota_count:
                    continue

            region = self.multiworld.get_region(loc_data.region, self.player)
            loc = ContentWarningLocation(
                self.player, loc_name, location_name_to_id[loc_name], region
            )

            # Mark certain locations as EXCLUDED so AP never places
            # progression items there.
            stage = loc_data.game_stage
            if stage == "filler":
                loc.progress_type = LocationProgressType.EXCLUDED
            elif stage == "difficult" and not options.difficult_monsters.value:
                loc.progress_type = LocationProgressType.EXCLUDED
            elif loc_name in _HIGH_VIEW_MILESTONES and low_quota:
                # When quota goal is low, high-view milestones are unachievable
                # in a short run — only filler is placed there.
                loc.progress_type = LocationProgressType.EXCLUDED
            elif (
                loc_data.location_group == "Monster Tiers"
                and options.filler_multi_sightings.value
            ):
                # Filler Multi-Sightings option (default on): tier-2/tier-3
                # monster and artifact locations only hold filler items.
                loc.progress_type = LocationProgressType.EXCLUDED

            region.locations.append(loc)

        # Place the Victory event location + item in Sky Island.
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
        options = self.options
        return {
            # Primary goal
            "goal":                         sorted(options.goal.value),
            "views_goal_target":            int(options.views_goal_target.value),
            "monster_hunter_count":         int(options.monster_hunter_count.value),
            "hat_collector_count":          int(options.hat_collector_count.value),
            "item_collector_count":         int(options.item_collector_count.value),

            # Quota
            "quota_requirement":            bool(options.quota_requirement.value),
            "quota_count":                  int(options.quota_count.value),

            # Location group toggles
            "include_hats":                 bool(options.include_hats.value),
            "include_emotes":               bool(options.include_emotes.value),
            "include_sponsorships":         bool(options.include_sponsorships.value),
            "sponsorsanity":                bool(options.sponsorsanity.value),
            "difficult_monsters":           bool(options.difficult_monsters.value),
            "multiplayer_mode":             bool(options.multiplayer_mode.value),
            "monster_tiers":                bool(options.monster_tiers.value),
            "filler_multi_sightings":       bool(options.filler_multi_sightings.value),
        }
