# Content Warning Archipelago Integration

This repository contains the Archipelago Multiworld Randomizer integration for *Content Warning*. 

## 📥 APWorld Installation
1. **Download** the `content_warning.apworld` file.
2. **Move** the file into your local Archipelago custom worlds folder:

3. **Restart** your Archipelago launcher to ensure the game appears in the generation list.

## ⚙️ YAML Options Breakdown
Your YAML file allows you to customize the difficulty and settings of your world.

### Victory Conditions (Goal)
* **viral_sensation:** Reach the ultimate milestone of 1,000,000 views in one quota.
* **views_goal:** Reach a custom amount of total views over multiple runs. 
* **quota_goal:** Reach a set number of quotas to win.
* **monster_hunter:** Win by filming a specific number of unique monsters.
* **hat_collector:** Purchase a configurable number of hats.


### Check Options
* **views_checks:** When enabled, lifetime-view milestone locations are part of the pool. If disabled, all view threshold locations are removed from generation and the Views Goal becomes invalid.
* **views_goal_target:** Sets the lifetime view total required to win if the Views Goal is enabled, up to a maximum of 33,739,000 views.
* **quota_requirement:** Includes quota checks in the location pool. If disabled, all quota-related checks are removed and the Quota Goal becomes invalid.
* **quota_count:** Determines the number of quotas to play through, ranging from 1 to 21. This setting drives the active count of Quota, Extracted on Day X, and Sponsorship locations.
* **monster_hunter_count:** Sets the required number of distinct monsters that must be filmed to achieve the Monster Hunter Goal, ranging from 5 to 33.
* **monster_tiers:** Gives each non-difficult filmable monster two additional filming location checks for their 2nd and 3rd sightings. This adds up to 42 extra location checks to your world.
* **filler_multi_sightings:** When enabled alongside Monster Tiers, all 2nd and 3rd sighting locations will only hold filler items, preventing progression items from spawning there.
* **difficult_monsters:** Allows difficult or rare monsters (such as the Flicker, Cam Creep, Infiltrator, Black Hole Bot, Ear, Snail Spawner, Big Slap, Ultra Knifo, and Weeping) to have real, non-filler items hidden behind their base filming checks.
* **hat_collector_count:** Sets the number of hats that must be purchased to achieve the Hat Collector Goal, ranging from 5 to 31.
* **include_sponsorships:** Adds sponsorship checks into the location pool. Each completed sponsorship grants the next check in order, capped at 20 total based on quota count.
* **sponsor_filler:** Forces all sponsor locations to contain only filler items, keeping progression items away from RNG-dependent sponsorships.
* **multiplayer_mode:** Adds multiplayer-only monster locations, such as the Weeping, into the world generation pool so they can receive items. If playing solo, leave this disabled so those locations are completely omitted from generation.


## 🚀 How to Generate
1. Open your `Content Warning.yaml` and set your `name`.
2. Adjust your preferred goals and settings.
3. Place the YAML in your Archipelago `Players` folder along with other player's YAML files.
4. Run the generate command on the Archipelago launcher
5. The output file will be in your outputs folder.
