# location names referenced in locations.py / rules.py

# ---- Extractions ----
any_extraction            = "Any Extraction"
extracted_footage_prefix  = "Extracted Footage on Day "   # + str(day_number), 1..63

# ---- Quotas ----
met_quota_prefix = "Met Quota "   # + str(quota_number), 1..21

# ---- View Milestones ----
# Lifetime-total milestones; one per in-game day (1..63).  See VIEW_MILESTONES
# in locations.py for the canonical (day, lifetime_total, quota) table.

def reached_total_views(total: int) -> str:
    """Canonical name for a lifetime-views milestone location."""
    return f"Reached {total:,} Total Views"


# ---- Sponsorships ----
# After issue #5 the trigger is per-completion (mod-side).  Active count per
# seed is QuotaCount - 1, capped at 20.
completed_sponsorship_prefix = "Completed Sponsorship "   # + str(N), 1..20

# ---- Found Chorby ----
# Issue #11 (mod #14): one Chorby spawns per dive; pickup is intercepted and
# fires the next sequential Found Chorby N location.  Active count per seed is
# QuotaCount (1..21); counter persists across run loss/restart on the mod side.
found_chorby_prefix = "Found Chorby "   # + str(N), 1..21

# ---- Viral Sensation event ----
# Client-emitted check fired when the player crosses 1,000,000 views in a
# single quota.  Only added to the world when the viral_sensation goal is on.
viral_sensation_achieved = "Viral Sensation Achieved"

# ---- Victory ----
victory = "Victory"
