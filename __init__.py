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
    VIEW_MILESTONES, LIFETIME_VIEWS_BY_DAY, MAX_LIFETIME_VIEWS,
    _DIFFICULT_MONSTERS,
)
from .regions import CW_regions
from .rules import set_region_rules, set_location_rules
from .options import ContentWarningGameOptions
from .names import item_names as iname, location_names as lname, region_names as rname

# Monster locations that require Multiplayer Mode (player_count > 1).
# In solo seeds these locations are skipped entirely in create_regions — the
# player cannot encounter the monster without other players in the lobby, so
# leaving the check in the world (even as filler) would strand any item
# placed there.
_MULTIPLAYER_ONLY_MONSTERS = {
    "Filmed Weeping",
}

# Tier 2/3 of multiplayer-only monsters inherit the same gate.
_MULTIPLAYER_ONLY_LOCATIONS = (
    set(_MULTIPLAYER_ONLY_MONSTERS)
    | {f"{m} 2" for m in _MULTIPLAYER_ONLY_MONSTERS}
    | {f"{m} 3" for m in _MULTIPLAYER_ONLY_MONSTERS}
)


def _base_monster_name(tier_name: str) -> str:
    """'Filmed Worm 2' / 'Filmed Worm 3' -> 'Filmed Worm'.  Returns the
    input unchanged if it doesn't end in ' 2' or ' 3'."""
    if tier_name.endswith(" 2") or tier_name.endswith(" 3"):
        return tier_name[:-2]
    return tier_name


def _max_active_view_total(quota_on: bool, quota_count: int,
                           views_goal_on: bool, views_target: int) -> int:
    """Cap for active view-milestone locations.

    Per Jake's clarification on issue #4 (D): include all milestones up to
    max(milestone_at_day(QuotaCount * 3), nearest_milestone_at_or_above(target)).
    If the views_goal toggle is off, the second term doesn't apply.
    If quota_requirement is off, no quota-based cap — the player can play
    indefinitely, so use the full table.
    """
    if not quota_on:
        day_cap = MAX_LIFETIME_VIEWS
    else:
        max_day = min(quota_count * 3, 63)
        day_cap = LIFETIME_VIEWS_BY_DAY[max_day]

    if not views_goal_on:
        return day_cap

    target_cap = 0
    for _, total, _ in VIEW_MILESTONES:
        if total >= views_target:
            target_cap = total
            break
    if target_cap == 0:
        target_cap = MAX_LIFETIME_VIEWS  # target above the table — clamp to top

    return max(day_cap, target_cap)


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
        """How many 'Monsters' group locations are logically reachable given
        the current option settings.

        Excludes:
          • Multiplayer-only monsters (Weeping) when multiplayer_mode is off.
          • Difficult-stage monsters when difficult_monsters is off.
        """
        options = self.options
        return sum(
            1 for name, data in location_table.items()
            if data.location_group == "Monsters"
            and not (name in _MULTIPLAYER_ONLY_MONSTERS and not options.multiplayer_mode.value)
            and not (data.game_stage == "difficult" and not options.difficult_monsters.value)
        )

    def _active_view_milestone_names(self) -> List[str]:
        """View-milestone location names included in the current generation."""
        options = self.options
        if not options.views_checks.value:
            return []
        cap = _max_active_view_total(
            quota_on=bool(options.quota_requirement.value),
            quota_count=options.quota_count.value,
            views_goal_on=bool(options.views_goal.value),
            views_target=int(options.views_goal_target.value),
        )
        return [
            lname.reached_total_views(total)
            for _, total, _ in VIEW_MILESTONES
            if total <= cap
        ]

    def _active_sponsor_count(self) -> int:
        """Sponsorship checks active in the current generation."""
        options = self.options
        if not options.include_sponsorships.value:
            return 0
        return min(max(0, options.quota_count.value - 1), 20)

    def _active_day_count(self) -> int:
        """Day-extraction checks active in the current generation.  Capped to
        QuotaCount * 3 (= 63 at QuotaCount=21).  When quota_requirement is
        off, day checks aren't gated by quota progression; we still respect
        QuotaCount to bound the world."""
        options = self.options
        return min(max(0, options.quota_count.value * 3), 63)

    def _compute_location_total(self) -> int:
        """The real number of check locations create_regions will produce."""
        options = self.options
        quota_on    = bool(options.quota_requirement.value)
        quota_count = options.quota_count.value if quota_on else 0
        active_views = set(self._active_view_milestone_names())
        active_sponsors = self._active_sponsor_count()
        active_days = self._active_day_count()
        viral_on = bool(options.viral_sensation.value)

        total = 0
        for loc_name, loc_data in location_table.items():
            if loc_data.location_group in (None, "Event"):
                continue
            if loc_data.location_id_offset is None:
                continue

            grp = loc_data.location_group

            if grp == "Sponsorships":
                num = int(loc_name.replace(lname.completed_sponsorship_prefix, ""))
                if num > active_sponsors:
                    continue

            if grp == "Days":
                num = int(loc_name.replace(lname.extracted_footage_prefix, ""))
                if num > active_days:
                    continue

            if grp == "Quotas":
                num = int(loc_name.replace(lname.met_quota_prefix, ""))
                if num > quota_count:
                    continue

            if grp == "Views":
                if loc_name not in active_views:
                    continue

            if grp == "Monster Tiers" and not options.monster_tiers.value:
                continue

            if grp == "Viral Sensation" and not viral_on:
                continue

            if loc_name in _MULTIPLAYER_ONLY_LOCATIONS and not options.multiplayer_mode.value:
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
        """Clamp option values that depend on runtime-computed reachable counts."""
        options = self.options

        # Cap monster_hunter_count to actually-reachable monsters.
        if options.monster_hunter.value:
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
        items_to_create: Dict[str, int] = {
            name: data.quantity_in_item_pool
            for name, data in item_table.items()
            if data.item_group != "Event"
        }

        named_total: int = sum(items_to_create.values())
        total_filler = max(0, self.location_total - named_total)

        # Guaranteed minimum money pool — pool-count interpretation per issue #3.
        # Early ($1,000):  4×$50 + 8×$100
        # Mid   ($1,000):  4×$50 + 4×$100 + 2×$200
        # Late  ($2,200):  4×$50 + 2×$100 + 3×$200 + 3×$400
        money_minimums: Dict[str, int] = {
            iname.money_50:  4 + 4 + 4,   # 12
            iname.money_100: 8 + 4 + 2,   # 14
            iname.money_200: 0 + 2 + 3,   # 5
            iname.money_400: 0 + 0 + 3,   # 3
        }
        for name, count in money_minimums.items():
            for _ in range(count):
                cw_items.append(self.create_item(name))

        total_filler -= sum(money_minimums.values())

        # Remaining slots are filled with weighted money filler.
        for _ in range(total_filler):
            cw_items.append(self.create_item(self.random.choice(MONEY_FILLER_POOL)))

        # Add all named items.
        for name, quantity in items_to_create.items():
            for _ in range(quantity):
                cw_items.append(self.create_item(name))

        self.multiworld.itempool += cw_items

        # Push small Meta Coin packages into sphere-1 locations so the early
        # budget is accessible before mid/late items unlock.
        early_items = self.multiworld.early_items[self.player]
        early_items[iname.meta_coins_500]  = 3
        early_items[iname.meta_coins_1000] = 2

    # -----------------------------------------------------------------------
    # Regions & Locations
    # -----------------------------------------------------------------------

    def create_regions(self) -> None:
        options = self.options
        quota_on    = bool(options.quota_requirement.value)
        quota_count = options.quota_count.value if quota_on else 0
        viral_on    = bool(options.viral_sensation.value)
        sponsor_on  = bool(options.include_sponsorships.value)
        sponsor_filler = bool(options.sponsor_filler.value)

        active_views = set(self._active_view_milestone_names())
        active_sponsors = self._active_sponsor_count()
        active_days = self._active_day_count()

        # Build set of disabled location groups.
        disabled_groups: set = set()
        if not options.monster_tiers.value:
            disabled_groups.add("Monster Tiers")
        if not options.views_checks.value:
            disabled_groups.add("Views")
        if not sponsor_on:
            disabled_groups.add("Sponsorships")
        if not viral_on:
            disabled_groups.add("Viral Sensation")

        # Create all regions and wire exits.
        for region_name in CW_regions:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
        for region_name, exits in CW_regions.items():
            self.multiworld.get_region(region_name, self.player).add_exits(exits)

        # Place each location into its region.
        for loc_name, loc_data in location_table.items():
            if loc_data.location_group == "Event":
                continue
            if loc_data.location_group in disabled_groups:
                continue

            # Solo seeds: completely omit multiplayer-only checks.
            if loc_name in _MULTIPLAYER_ONLY_LOCATIONS and not options.multiplayer_mode.value:
                continue

            grp = loc_data.location_group

            # Variable quota count: skip quotas beyond the configured number.
            if grp == "Quotas":
                if not quota_on:
                    continue
                num = int(loc_name.replace(lname.met_quota_prefix, ""))
                if num > quota_count:
                    continue

            # Day extractions: 1..QuotaCount*3.
            if grp == "Days":
                num = int(loc_name.replace(lname.extracted_footage_prefix, ""))
                if num > active_days:
                    continue

            # Sponsorships: 1..(QuotaCount-1, max 20).
            if grp == "Sponsorships":
                num = int(loc_name.replace(lname.completed_sponsorship_prefix, ""))
                if num > active_sponsors:
                    continue

            # Views: only milestones <= active cap.
            if grp == "Views" and loc_name not in active_views:
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
            elif grp == "Monster Tiers":
                # Tier 2/3 of difficult monsters are always filler-only,
                # regardless of DifficultMonsters or FillerMultiSightings
                # (issue #4 / #5 Q1+F).  Other tiers fall back to
                # FillerMultiSightings.
                base = _base_monster_name(loc_name)
                if base in _DIFFICULT_MONSTERS:
                    loc.progress_type = LocationProgressType.EXCLUDED
                elif options.filler_multi_sightings.value:
                    loc.progress_type = LocationProgressType.EXCLUDED
            elif grp == "Sponsorships" and sponsor_filler:
                loc.progress_type = LocationProgressType.EXCLUDED
            elif grp == "Viral Sensation":
                # Goal-trigger location — fired by the client when the
                # player crosses 1M views in a single quota.  No progression
                # items here; only filler.  The viral_sensation goal rule
                # (rules.py) gates reachability on Progressive Views items.
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
            # Goal toggles (replaces the old single 'goal' set)
            "viral_sensation":              bool(options.viral_sensation.value),
            "views_goal":                   bool(options.views_goal.value),
            "quota_goal":                   bool(options.quota_goal.value),
            "monster_hunter":               bool(options.monster_hunter.value),
            "hat_collector":                bool(options.hat_collector.value),

            # Counts / thresholds
            "views_goal_target":            int(options.views_goal_target.value),
            "monster_hunter_count":         int(options.monster_hunter_count.value),
            "hat_collector_count":          int(options.hat_collector_count.value),

            # Quota
            "quota_requirement":            bool(options.quota_requirement.value),
            "quota_count":                  int(options.quota_count.value),

            # View / sponsor / monster toggles
            "views_checks":                 bool(options.views_checks.value),
            "include_sponsorships":         bool(options.include_sponsorships.value),
            "sponsor_filler":               bool(options.sponsor_filler.value),
            "difficult_monsters":           bool(options.difficult_monsters.value),
            "monster_tiers":                bool(options.monster_tiers.value),
            "filler_multi_sightings":       bool(options.filler_multi_sightings.value),
            "multiplayer_mode":             bool(options.multiplayer_mode.value),
        }
