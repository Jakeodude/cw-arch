# worlds/content_warning/rules.py

from typing import TYPE_CHECKING, List, Tuple
from worlds.generic.Rules import add_rule

from .names import location_names as lname
from .names import region_names as rname
from .locations import location_table
from . import logic

if TYPE_CHECKING:
    from . import ContentWarningWorld


# ---------------------------------------------------------------------------
# View milestone order and Progressive Views thresholds
# ---------------------------------------------------------------------------
_VIEW_MILESTONE_ORDER: List[Tuple[int, str]] = [
    (1_000,   lname.reached_1k),
    (2_000,   lname.reached_2k),
    (3_000,   lname.reached_3k),
    (13_000,  lname.reached_13k),
    (26_000,  lname.reached_26k),
    (39_000,  lname.reached_39k),
    (43_000,  lname.reached_43k),
    (85_000,  lname.reached_85k),
    (128_000, lname.reached_128k),
    (150_000, lname.reached_150k),
    (220_000, lname.reached_220k),
    (325_000, lname.reached_325k),
    (375_000, lname.reached_375k),
    (430_000, lname.reached_430k),
    (645_000, lname.reached_645k),
    (850_000, lname.reached_850k),
    (1_000_000, lname.reached_1m),
]

# How many Progressive Views items are required before each higher milestone
# is considered logically reachable (lower milestones need none).
_VIEW_THRESHOLDS = {
    lname.reached_85k:  2,
    lname.reached_128k: 3,
    lname.reached_150k: 4,
    lname.reached_220k: 5,
    lname.reached_325k: 6,
    lname.reached_375k: 7,
    lname.reached_430k: 8,
    lname.reached_645k: 10,
    lname.reached_850k: 11,
    lname.reached_1m:   12,
}


def _get_views_goal_milestone(target: int) -> str:
    """Return the location name of the nearest view milestone at or above target."""
    for views, loc_name in _VIEW_MILESTONE_ORDER:
        if views >= target:
            return loc_name
    return lname.reached_1m  # fallback


# ---------------------------------------------------------------------------
# Region rules
# ---------------------------------------------------------------------------

def set_region_rules(world: "ContentWarningWorld") -> None:
    """Set entrance access rules between regions."""
    multiworld = world.multiworld
    player = world.player

    # Sky Island is always accessible from Menu — no rule needed.

    # The Old World requires a Progressive Camera to enter.
    multiworld.get_entrance(
        f"{rname.hub} -> {rname.dungeon}", player
    ).access_rule = lambda state: logic.can_enter_dungeon(state, player)


# ---------------------------------------------------------------------------
# Location rules
# ---------------------------------------------------------------------------

def set_location_rules(world: "ContentWarningWorld") -> None:
    """Set individual location access rules and the completion condition."""
    multiworld = world.multiworld
    player = world.player
    options = world.options

    quota_on    = bool(options.quota_requirement.value)
    quota_count = options.quota_count.value

    # -----------------------------------------------------------------------
    # Completion condition
    # -----------------------------------------------------------------------
    multiworld.completion_condition[player] = lambda state: state.has(
        lname.victory, player
    )
    victory_loc = multiworld.get_location(lname.victory, player)

    # -----------------------------------------------------------------------
    # Primary Goal rules (all selected goals must be satisfied)
    # -----------------------------------------------------------------------
    goal = options.goal.value  # frozenset of selected goal strings

    if "viral_sensation" in goal:
        # Reach the 1,000,000 view milestone.
        add_rule(victory_loc, lambda state: logic.has_views(state, player, 12))

    if "views_goal" in goal:
        # Reach the nearest milestone at or above the configured target.
        milestone = _get_views_goal_milestone(options.views_goal_target.value)
        threshold = _VIEW_THRESHOLDS.get(milestone, 0)
        if threshold:
            add_rule(
                victory_loc,
                lambda state, t=threshold: logic.has_views(state, player, t),
            )
        add_rule(
            victory_loc,
            lambda state, m=milestone: state.can_reach_location(m, player),
        )

    if "quota_goal" in goal:
        # Must reach and complete quota N (requires Quota Requirement on).
        if quota_on and quota_count >= 1:
            nth_quota = lname.met_quota_prefix + str(quota_count)
            add_rule(
                victory_loc,
                lambda state, q=nth_quota: state.can_reach_location(q, player),
            )
        else:
            # Quota disabled — require viral sensation as fallback
            add_rule(victory_loc, lambda state: logic.has_views(state, player, 12))

    if "monster_hunter" in goal:
        count = options.monster_hunter_count.value
        monster_locs: List[str] = [
            n for n, d in location_table.items()
            if d.location_group == "Monsters"
        ]
        add_rule(
            victory_loc,
            lambda state, c=count, locs=monster_locs:
                logic.count_reachable(state, player, locs) >= c,
        )

    # hat_collector is skipped when Include Hat Purchases is disabled,
    # since no hat locations exist in the pool.
    if "hat_collector" in goal and options.include_hats.value:
        count = options.hat_collector_count.value
        hat_locs: List[str] = [
            n for n, d in location_table.items()
            if d.location_group == "Hats"
        ]
        add_rule(
            victory_loc,
            lambda state, c=count, locs=hat_locs:
                logic.count_reachable(state, player, locs) >= c,
        )

    # item_collector is skipped when Include Emote Purchases is disabled,
    # since emote locations are removed from the pool.
    if "item_collector" in goal and options.include_emotes.value:
        count = options.item_collector_count.value
        item_locs: List[str] = [
            n for n, d in location_table.items()
            if d.location_group in ("Store Purchases", "Emotes")
        ]
        add_rule(
            victory_loc,
            lambda state, c=count, locs=item_locs:
                logic.count_reachable(state, player, locs) >= c,
        )

    # -----------------------------------------------------------------------
    # View milestone rules
    # -----------------------------------------------------------------------
    for milestone, threshold in _VIEW_THRESHOLDS.items():
        # Skip milestones ≥128k if quota count < 4 (only filler placed there;
        # the item placement in __init__.py enforces the filler, but we still
        # need to allow access so locations can be reached for the goal).
        add_rule(
            multiworld.get_location(milestone, player),
            lambda state, t=threshold: logic.has_views(state, player, t),
        )

    # -----------------------------------------------------------------------
    # Dungeon depth rules (mid / late stage checks)
    # -----------------------------------------------------------------------
    for loc_name, loc_data in location_table.items():
        if loc_data.region != rname.dungeon:
            continue
        # Monster Tier locations are only created when the MonsterTiers option
        # is enabled.  Skip them here to avoid a KeyError when the option is off.
        if loc_data.location_group == "Monster Tiers" and not options.monster_tiers.value:
            continue

        if loc_data.game_stage == "mid":
            add_rule(
                multiworld.get_location(loc_name, player),
                lambda state: logic.can_explore_mid_dungeon(state, player),
            )
        elif loc_data.game_stage in ("late", "difficult"):
            add_rule(
                multiworld.get_location(loc_name, player),
                lambda state: logic.can_explore_late_dungeon(state, player),
            )

    # -----------------------------------------------------------------------
    # Multiplayer-only monster rules
    # "Filmed Weeping" and "Filmed Worm" require Multiplayer Mode to be on.
    # When Multiplayer Mode is off these locations are already marked EXCLUDED
    # in create_regions; the rule here enforces the logic constraint so AP
    # never treats them as reachable in solo seeds.
    #
    # "Filmed Worm 2" / "Filmed Worm 3" (Monster Tier locations) also inherit
    # the multiplayer requirement; they only exist when MonsterTiers is on.
    # -----------------------------------------------------------------------
    _MULTIPLAYER_ONLY: set = {"Filmed Weeping", "Filmed Worm"}
    multiplayer_on = bool(options.multiplayer_mode.value)

    # Base locations are always present in the multiworld (marked EXCLUDED in
    # solo seeds but never omitted entirely).  Wrapped in try/except as a
    # belt-and-suspenders guard against future option combinations.
    for mp_loc in _MULTIPLAYER_ONLY:
        try:
            add_rule(
                multiworld.get_location(mp_loc, player),
                lambda state, mp=multiplayer_on: mp,
            )
        except KeyError:
            pass  # location not present in this generation — skip

    # Worm tier locations only exist when MonsterTiers is enabled.
    if options.monster_tiers.value:
        for tier_num in (2, 3):
            worm_tier = f"Filmed Worm {tier_num}"
            add_rule(
                multiworld.get_location(worm_tier, player),
                lambda state, mp=multiplayer_on: mp,
            )

    # -----------------------------------------------------------------------
    # Quota rules: each quota N requires quota N-1 to be reachable.
    # Only create rules for quotas that are actually in the pool.
    # -----------------------------------------------------------------------
    if quota_on:
        for i in range(2, quota_count + 1):
            prev = lname.met_quota_prefix + str(i - 1)
            curr = lname.met_quota_prefix + str(i)
            add_rule(
                multiworld.get_location(curr, player),
                lambda state, p=prev: state.can_reach_location(p, player),
            )

    # -----------------------------------------------------------------------
    # Day extraction rules: each day requires the previous.
    # -----------------------------------------------------------------------
    for i in range(2, 16):
        prev = lname.extracted_footage_prefix + str(i - 1)
        curr = lname.extracted_footage_prefix + str(i)
        add_rule(
            multiworld.get_location(curr, player),
            lambda state, p=prev: state.can_reach_location(p, player),
        )
