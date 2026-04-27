# worlds/content_warning/options.py

from dataclasses import dataclass
from Options import OptionSet, Toggle, DefaultOnToggle, Range, PerGameCommonOptions


# ===========================================================================
# GOAL
# ===========================================================================

class GoalChoice(OptionSet):
    """Choose one or more victory conditions. All selected conditions must be
    completed to win. Select any combination from the list below.

    viral_sensation:  Reach 1,000,000 total views — the highest view milestone.
    views_goal:       Reach a configurable total view count (see Views Goal Target).
    quota_goal:       Reach and complete a configurable number of quotas
                      (see Quota Requirement and Quota Count; requires Quota Requirement on).
    monster_hunter:   Film a configurable number of different monsters (see Monster Hunter Count).
    hat_collector:    Purchase a configurable number of hats (see Hat Collector Count).
                      Note: automatically ignored if Include Hat Purchases is disabled.
    item_collector:   Purchase a configurable number of store items and emotes
                      (see Item Collector Count).
                      Note: automatically ignored if Include Emote Purchases is disabled."""
    display_name = "Goal"
    valid_keys = frozenset({
        "viral_sensation",
        "views_goal",
        "quota_goal",
        "monster_hunter",
        "hat_collector",
        "item_collector",
    })
    default = frozenset({"viral_sensation"})


class ViewsGoalTarget(Range):
    """When Goal is 'views_goal', this sets the required total views to win.
    The game uses the nearest view milestone at or above the configured value.
    Ignored when Goal is not 'views_goal'."""
    display_name = "Views Goal Target"
    range_start  = 1000
    range_end    = 1000000
    default      = 128000


class MonsterHunterCount(Range):
    """When Goal is 'monster_hunter', the number of different monsters that must
    be filmed to win. Minimum 5, maximum 33.
    Note: an average 5-quota run encounters an average of 15-20 monsters."""
    display_name = "Monster Hunter Count"
    range_start  = 5
    range_end    = 33
    default      = 12


class HatCollectorCount(Range):
    """When Goal is 'hat_collector', the number of hats that must be purchased
    to win. Minimum 5, maximum 31 (total hats available).
    Ignored when Include Hat Purchases is disabled (hat_collector goal is inactive)."""
    display_name = "Hat Collector Count"
    range_start  = 5
    range_end    = 31
    default      = 15


class ItemCollectorCount(Range):
    """When Goal is 'item_collector', the number of store items and emotes that
    must be purchased to win. Minimum 5, maximum 33.
    Ignored when Include Emote Purchases is disabled (item_collector goal is inactive)."""
    display_name = "Item Collector Count"
    range_start  = 5
    range_end    = 33
    default      = 10


# ===========================================================================
# QUOTA
# ===========================================================================

class QuotaRequirement(DefaultOnToggle):
    """When enabled, quota checks are included in the location pool and
    completing quotas can be part of the goal.
    When disabled, ALL quota-related checks are removed from the pool
    (the 'quota_goal' Goal option becomes invalid and falls back to
    'viral_sensation')."""
    display_name = "Quota Requirement"


class QuotaCount(Range):
    """The number of quotas that must be reached and completed.
    Controls both how many quota locations exist in the pool and (if
    Goal is 'quota_goal') how many are required to win.
    Minimum 1, maximum 10.
    Requires Quota Requirement to be enabled."""
    display_name = "Quota Count"
    range_start  = 1
    range_end    = 10
    default      = 5


# ===========================================================================
# OPTIONAL LOCATION GROUPS
# ===========================================================================

class IncludeHats(DefaultOnToggle):
    """When enabled, purchasing each hat from Phil's Hat Shop is a check location.
    Disable to remove all hat locations from the pool."""
    display_name = "Include Hat Purchases"


class IncludeEmotes(DefaultOnToggle):
    """When enabled, purchasing each emote from the store is a check location.
    Disable to remove all emote locations from the pool."""
    display_name = "Include Emote Purchases"


class IncludeSponsorship(DefaultOnToggle):
    """When enabled, accepting sponsorships (3 checks) are check locations.
    Disable to remove all sponsorship acceptance locations from the pool."""
    display_name = "Include Sponsorships"


class Sponsorsanity(Toggle):
    """When enabled, completing each sponsorship difficulty
    (Easy, Medium, Hard, Very Hard) adds extra check locations.
    Requires Include Sponsorships to be enabled."""
    display_name = "Sponsorsanity"


class DifficultMonsters(Toggle):
    """When enabled, difficult/rare monsters (Flicker, Cam Creep, Infiltrator,
    Black Hole Bot, Ear, Snail Spawner, Big Slap, Ultra Knifo) can
    have real (non-filler) items behind their filming checks.
    When disabled (default), those checks always contain filler rewards."""
    display_name = "Difficult Monsters Have Real Items"


class MultiplayerMode(Toggle):
    """Enable if this game is being played in multiplayer (more than one player).
    When enabled, multiplayer-only monster locations (Weeping) are added to
    the world and can receive real items.
    When disabled (default / solo play), those locations are completely
    omitted from generation — the player would never be able to film them
    without other players in the lobby."""
    display_name = "Multiplayer Mode"


class MonsterTiers(Toggle):
    """When enabled, each non-difficult filmable monster gains two additional
    filming location checks — Tier 2 and Tier 3 — representing multiple
    encounters with the same monster across different dives.
    No additional logic requirements apply beyond those of the base check
    (dungeon depth rules still apply based on the monster's game stage).
    Adds up to 42 new check locations to the pool."""
    display_name = "Monster Tiers"


class FillerMultiSightings(DefaultOnToggle):
    """When enabled, all monster and artifact tier-2 / tier-3 locations
    (the 'Monster Tiers' group, created by the Monster Tiers option) hold
    only filler items — no progression or useful items are placed there.
    The locations themselves still exist; only their item classification is
    constrained.  Disable to let real items spawn behind multi-sighting
    checks, increasing item-pool density at the cost of more required dives.
    Has no effect when Monster Tiers is disabled."""
    display_name = "Filler Multi-Sightings"


# ===========================================================================
# OPTIONS DATACLASS
# ===========================================================================

@dataclass
class ContentWarningGameOptions(PerGameCommonOptions):
    # Goal
    goal:                       GoalChoice
    views_goal_target:          ViewsGoalTarget
    monster_hunter_count:       MonsterHunterCount
    hat_collector_count:        HatCollectorCount
    item_collector_count:       ItemCollectorCount

    # Quota
    quota_requirement:          QuotaRequirement
    quota_count:                QuotaCount

    # Optional location groups
    include_hats:           IncludeHats
    include_emotes:         IncludeEmotes
    include_sponsorships:   IncludeSponsorship
    sponsorsanity:          Sponsorsanity
    difficult_monsters:     DifficultMonsters
    multiplayer_mode:       MultiplayerMode
    monster_tiers:          MonsterTiers
    filler_multi_sightings: FillerMultiSightings
