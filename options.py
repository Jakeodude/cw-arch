# worlds/content_warning/options.py

from dataclasses import dataclass
from Options import Choice, Toggle, DefaultOnToggle, PerGameCommonOptions


class GoalChoice(Choice):
    """Choose the victory condition for your run.

    viral_sensation: Reach 645,000 total views — the highest view milestone.
    content_complete: Film every monster and every artifact at least once."""
    display_name = "Goal"
    option_viral_sensation  = 0
    option_content_complete = 1
    default = 0


class IncludeHats(DefaultOnToggle):
    """When enabled, purchasing each hat from Phil's Hat Shop is a check location.
    Disable to remove all 31 hat locations from the pool."""
    display_name = "Include Hat Purchases"


class IncludeEmotes(DefaultOnToggle):
    """When enabled, purchasing each emote from the store is a check location.
    Disable to remove all 16 emote locations from the pool."""
    display_name = "Include Emote Purchases"


class IncludeSponsorship(DefaultOnToggle):
    """When enabled, accepting and completing sponsorships are check locations.
    Disable to remove the 4 sponsorship locations from the pool."""
    display_name = "Include Sponsorships"


class DungeonLogic(Choice):
    """How strictly survival gear is logically required to access dungeon checks.

    easy:  Shock Stick and health/oxygen upgrades are required before dangerous
           monster filming locations are in logic.
    hard:  Nothing is required; the player may face dangerous situations without
           safety equipment."""
    display_name = "Dungeon Logic"
    option_easy = 0
    option_hard = 1
    default = 0


@dataclass
class ContentWarningGameOptions(PerGameCommonOptions):
    goal:                GoalChoice
    include_hats:        IncludeHats
    include_emotes:      IncludeEmotes
    include_sponsorships: IncludeSponsorship
    dungeon_logic:       DungeonLogic
