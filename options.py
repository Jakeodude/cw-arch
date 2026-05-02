# worlds/content_warning/options.py

from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Range, PerGameCommonOptions


# ===========================================================================
# GOAL TOGGLES
#
# Any combination of goal toggles may be enabled.  All enabled goals must be
# satisfied to win (AND semantics).  At least one goal should be on; by
# default ViralSensation is on so a fresh YAML always has a winnable seed.
# ===========================================================================

class ViralSensation(DefaultOnToggle):
    """Reach 1,000,000 views in a single quota.
    Fired by the client when the threshold is crossed in-game."""
    display_name = "Viral Sensation Goal"


class ViewsGoal(Toggle):
    """Reach the configurable lifetime view target (Views Goal Target).
    Requires Views Checks to be enabled — if Views Checks is off, this
    goal is treated as off."""
    display_name = "Views Goal"


class ViewsChecks(DefaultOnToggle):
    """When enabled, lifetime-view milestone locations are part of the pool.
    Disable to remove all view threshold locations from generation.
    If off, views_goal is invalid."""
    display_name = "Views Checks"


class ViewsGoalTarget(Range):
    """When Views Goal is enabled, the lifetime view total required to win.
    The world uses the nearest lifetime-view milestone at or above this value.
    Maximum 33,739,000 — the highest reachable lifetime total at the maximum
    quota count (day 63)."""
    display_name = "Views Goal Target"
    range_start  = 0
    range_end    = 33_739_000
    default      = 500_000


class QuotaGoal(Toggle):
    """Reach and complete the configured number of quotas.
    Requires Quota Requirement to be enabled — if Quota Requirement is off,
    this goal is treated as off."""
    display_name = "Quota Goal"


class QuotaRequirement(DefaultOnToggle):
    """When enabled, quota checks are included in the location pool and
    completing quotas can be part of the goal.
    When disabled, all quota-related checks are removed from the pool.
    If turned off, the Quota Goal will be invalid."""
    display_name = "Quota Requirement"


class QuotaCount(Range):
    """The number of quotas to play through.  Drives the active count of
    Quota / Day Extraction / Sponsorship locations and (if Quota Goal is on)
    the number required to win.
    Each quota is 3 days, so day-extraction checks run from day 1 to
    QuotaCount * 3.  Sponsorship checks run from 1 to QuotaCount - 1
    (capped at 20)."""
    display_name = "Quota Count"
    range_start  = 1
    range_end    = 21
    default      = 5


class MonsterHunter(Toggle):
    """Film a configurable number of distinct monsters (Monster Hunter Count)
    to win."""
    display_name = "Monster Hunter Goal"


class MonsterHunterCount(Range):
    """When Monster Hunter is enabled, the number of distinct monsters that
    must be filmed to win.  Minimum 5, maximum 33.
    Note: an average 5-quota run encounters 15-20 monsters."""
    display_name = "Monster Hunter Count"
    range_start  = 5
    range_end    = 33
    default      = 12


class MonsterTiers(Toggle):
    """When enabled, each non-difficult filmable monster gains two additional
    filming location checks (2nd and 3rd sightings).  Adds up to 42 extra
    location checks across non-difficult monsters and artifacts.  No new
    logic is added beyond the dungeon-depth rules of the base check."""
    display_name = "Monster Tiers"


class FillerMultiSightings(DefaultOnToggle):
    """When enabled, all 2nd / 3rd sighting locations created by Monster
    Tiers hold filler items only — no progression items spawn there.
    Disable to let real items spawn behind multi-sighting checks at the
    cost of more required dives.  No effect when Monster Tiers is off."""
    display_name = "Filler Multi-Sightings"


class DifficultMonsters(Toggle):
    """When enabled, difficult/rare monsters (Flicker, Cam Creep, Infiltrator,
    Black Hole Bot, Ear, Snail Spawner, Big Slap, Ultra Knifo, Weeping)
    can have real (non-filler) items behind their base filming checks.
    Tier 2 / Tier 3 of difficult monsters always remain filler regardless
    of this option."""
    display_name = "Difficult Monsters Have Real Items"


class HatCollector(Toggle):
    """Purchase a configurable number of hats (Hat Collector Count) to win."""
    display_name = "Hat Collector Goal"


class HatCollectorCount(Range):
    """When Hat Collector is enabled, the number of hats that must be
    purchased to win.  Minimum 5, maximum 31 (total hats available)."""
    display_name = "Hat Collector Count"
    range_start  = 5
    range_end    = 31
    default      = 15


class IncludeSponsorship(DefaultOnToggle):
    """When enabled, sponsorship checks are included in the pool.
    Each completed sponsorship grants the next sponsorship check in
    order; the active count per seed is QuotaCount - 1, capped at 20."""
    display_name = "Include Sponsorships"


class SponsorFiller(DefaultOnToggle):
    """When enabled (default), all sponsor locations contain filler items.
    Sponsorships are RNG-dependent and can be hard to complete; this keeps
    progression away from them by default.  Disable to let progression items
    spawn at sponsor locations."""
    display_name = "Sponsor Filler"


class MultiplayerMode(Toggle):
    """Enable if this game is played in multiplayer (more than one player).
    When enabled, multiplayer-only monster locations (Weeping) are added to
    the world and can receive real items.
    When disabled (default / solo play), those locations are completely
    omitted from generation — the player would never be able to film them
    without other players in the lobby."""
    display_name = "Multiplayer Mode"


# ===========================================================================
# OPTIONS DATACLASS
# ===========================================================================
# Order intentionally mirrors the spec in issue #5.

@dataclass
class ContentWarningGameOptions(PerGameCommonOptions):
    viral_sensation:        ViralSensation
    views_goal:             ViewsGoal
    views_checks:           ViewsChecks
    views_goal_target:      ViewsGoalTarget
    quota_goal:             QuotaGoal
    quota_requirement:      QuotaRequirement
    quota_count:            QuotaCount
    monster_hunter:         MonsterHunter
    monster_hunter_count:   MonsterHunterCount
    monster_tiers:          MonsterTiers
    filler_multi_sightings: FillerMultiSightings
    difficult_monsters:     DifficultMonsters
    hat_collector:          HatCollector
    hat_collector_count:    HatCollectorCount
    include_sponsorships:   IncludeSponsorship
    sponsor_filler:         SponsorFiller
    multiplayer_mode:       MultiplayerMode
