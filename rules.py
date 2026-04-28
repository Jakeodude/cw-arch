# worlds/content_warning/rules.py

from typing import TYPE_CHECKING, Dict, List
from worlds.generic.Rules import add_rule

from .names import location_names as lname
from .names import region_names as rname
from .locations import (
    location_table,
    VIEW_MILESTONES,
    MAX_LIFETIME_VIEWS,
)
from . import logic

if TYPE_CHECKING:
    from . import ContentWarningWorld


# ---------------------------------------------------------------------------
# View milestone access thresholds
# ---------------------------------------------------------------------------
# Total Progressive Views items in the pool — anchors the upper bound of the
# threshold curve below.  Must match items.py.
_TOTAL_PROG_VIEWS: int = 12

# Quotas at which the threshold ramp starts (inclusive lower bound) and ends
# (where it caps at _TOTAL_PROG_VIEWS).  Q1–Q3 are sphere-1 accessible
# (natural game progression); the ramp runs Q4..Q21.
_THRESHOLD_RAMP_START_QUOTA: int = 3
_THRESHOLD_RAMP_QUOTAS:      int = 21 - _THRESHOLD_RAMP_START_QUOTA  # 18


def _threshold_for_quota(quota: int) -> int:
    """Progressive Views items required to access a milestone whose lifetime
    total falls inside the given quota.

    Linear ramp from 0 at Q3 to _TOTAL_PROG_VIEWS at Q21, spread across the
    intervening 18 quotas.  Q1-Q3 always return 0 (sphere-1 access)."""
    n = quota - _THRESHOLD_RAMP_START_QUOTA
    if n <= 0:
        return 0
    return min(_TOTAL_PROG_VIEWS, n * _TOTAL_PROG_VIEWS // _THRESHOLD_RAMP_QUOTAS)


# Pre-computed: location_name -> required Progressive Views threshold.
_VIEW_THRESHOLDS: Dict[str, int] = {
    lname.reached_total_views(total): _threshold_for_quota(quota)
    for _, total, quota in VIEW_MILESTONES
}


def _get_views_goal_milestone(target: int) -> str:
    """Return the location name of the nearest lifetime-views milestone
    at or above target.  If target exceeds the table, returns the top
    milestone."""
    for _, total, _ in VIEW_MILESTONES:
        if total >= target:
            return lname.reached_total_views(total)
    return lname.reached_total_views(MAX_LIFETIME_VIEWS)


# ---------------------------------------------------------------------------
# Region rules
# ---------------------------------------------------------------------------

def set_region_rules(world: "ContentWarningWorld") -> None:
    """Set entrance access rules between regions."""
    multiworld = world.multiworld
    player = world.player

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
    views_checks_on = bool(options.views_checks.value)
    viral_on    = bool(options.viral_sensation.value)
    multiplayer_on = bool(options.multiplayer_mode.value)

    # -----------------------------------------------------------------------
    # Completion condition (stacked goals — AND semantics).
    # Every enabled goal toggle adds an independent rule to victory_loc.
    # -----------------------------------------------------------------------
    multiworld.completion_condition[player] = lambda state: state.has(
        lname.victory, player
    )
    victory_loc = multiworld.get_location(lname.victory, player)

    # ---- Viral Sensation goal ----
    # Goal is satisfied when the client-emitted "Viral Sensation Achieved"
    # event location can be reached.  Access to that location is gated below
    # on the full Progressive Views item count.
    if viral_on:
        add_rule(
            victory_loc,
            lambda state: state.can_reach_location(lname.viral_sensation_achieved, player),
        )

    # ---- Views Goal ----
    # Requires Views Checks to be on (otherwise the milestone location does
    # not exist in the world and the rule is unsatisfiable).  Silently
    # treated as off when views_checks is off.
    if options.views_goal.value and views_checks_on:
        milestone = _get_views_goal_milestone(int(options.views_goal_target.value))
        add_rule(
            victory_loc,
            lambda state, m=milestone: state.can_reach_location(m, player),
        )

    # ---- Quota Goal ----
    # Requires Quota Requirement to be on; silently off otherwise.
    if options.quota_goal.value and quota_on and quota_count >= 1:
        nth_quota = lname.met_quota_prefix + str(quota_count)
        add_rule(
            victory_loc,
            lambda state, q=nth_quota: state.can_reach_location(q, player),
        )

    # ---- Monster Hunter goal ----
    if options.monster_hunter.value:
        count = options.monster_hunter_count.value
        _mp_only = {"Filmed Weeping"}
        monster_locs: List[str] = [
            n for n, d in location_table.items()
            if d.location_group == "Monsters"
            and not (n in _mp_only and not multiplayer_on)
            and not (d.game_stage == "difficult" and not options.difficult_monsters.value)
        ]
        effective_count = min(count, len(monster_locs))
        add_rule(
            victory_loc,
            lambda state, c=effective_count, locs=monster_locs:
                logic.count_reachable(state, player, locs) >= c,
        )

    # ---- Hat Collector goal ----
    # Hats are now always in the pool (issue #5 — IncludeHats removed).
    if options.hat_collector.value:
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

    # -----------------------------------------------------------------------
    # View milestone access rules
    # Each milestone location's reachability is gated on Progressive Views.
    # Only set for milestones actually present in the world.
    # -----------------------------------------------------------------------
    if views_checks_on:
        for milestone_loc, threshold in _VIEW_THRESHOLDS.items():
            try:
                loc = multiworld.get_location(milestone_loc, player)
            except KeyError:
                continue  # not in this generation's pool
            if threshold > 0:
                add_rule(
                    loc,
                    lambda state, t=threshold: logic.has_views(state, player, t),
                )

    # -----------------------------------------------------------------------
    # Viral Sensation Achieved access rule
    # In-game the client fires this when the player crosses 1M views in a
    # single quota.  In AP logic we require all Progressive Views items as a
    # conservative gate — equivalent to the previous viral_sensation rule.
    # -----------------------------------------------------------------------
    if viral_on:
        try:
            vs_loc = multiworld.get_location(lname.viral_sensation_achieved, player)
        except KeyError:
            pass
        else:
            add_rule(
                vs_loc,
                lambda state: logic.has_views(state, player, _TOTAL_PROG_VIEWS),
            )

    # -----------------------------------------------------------------------
    # Dungeon depth rules (mid / late stage checks)
    # -----------------------------------------------------------------------
    for loc_name, loc_data in location_table.items():
        if loc_data.region != rname.dungeon:
            continue
        if loc_data.location_group == "Monster Tiers" and not options.monster_tiers.value:
            continue

        try:
            loc = multiworld.get_location(loc_name, player)
        except KeyError:
            continue  # not in this generation's pool

        if loc_data.game_stage == "mid":
            add_rule(loc, lambda state: logic.can_explore_mid_dungeon(state, player))
        elif loc_data.game_stage in ("late", "difficult"):
            add_rule(loc, lambda state: logic.can_explore_late_dungeon(state, player))

    # -----------------------------------------------------------------------
    # Multiplayer-only monster rules (semantic marker; locations are skipped
    # entirely in solo seeds).
    # -----------------------------------------------------------------------
    if multiplayer_on:
        for mp_loc in {"Filmed Weeping"}:
            try:
                add_rule(
                    multiworld.get_location(mp_loc, player),
                    lambda state: True,
                )
            except KeyError:
                pass

    # -----------------------------------------------------------------------
    # Quota chain rules: each quota N requires quota N-1 to be reachable.
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
    # Day extraction chain rules: each day requires the previous, up to the
    # active day count.
    # -----------------------------------------------------------------------
    active_days = min(quota_count * 3, 63)
    for i in range(2, active_days + 1):
        prev = lname.extracted_footage_prefix + str(i - 1)
        curr = lname.extracted_footage_prefix + str(i)
        try:
            curr_loc = multiworld.get_location(curr, player)
        except KeyError:
            continue
        add_rule(
            curr_loc,
            lambda state, p=prev: state.can_reach_location(p, player),
        )

    # -----------------------------------------------------------------------
    # Sponsorship chain rules: each sponsorship N requires sponsorship N-1.
    # Models the per-quota completion progression — at most one per quota,
    # so the player must finish prior sponsorships to access the next check.
    # -----------------------------------------------------------------------
    if options.include_sponsorships.value:
        active_sponsors = min(max(0, quota_count - 1), 20)
        for i in range(2, active_sponsors + 1):
            prev = lname.completed_sponsorship_prefix + str(i - 1)
            curr = lname.completed_sponsorship_prefix + str(i)
            try:
                curr_loc = multiworld.get_location(curr, player)
            except KeyError:
                continue
            add_rule(
                curr_loc,
                lambda state, p=prev: state.can_reach_location(p, player),
            )
