# Content Warning Archipelago Integration

This repository contains the Archipelago Multiworld Randomizer integration for *Content Warning*. 

## 📥 APWorld Installation
1. **Download** the `content_warning.apworld` file.
2. **Move** the file into your local Archipelago custom worlds folder:

3. **Restart** your Archipelago launcher to ensure the game appears in the generation list.

## ⚙️ YAML Options Breakdown
Your YAML file allows you to customize the difficulty and settings of your world.

### Victory Conditions (Goal)
* **viral_sensation:** Reach the ultimate milestone of 1,000,000 views in one run.
* **views_goal:** Reach a custom amount of total views over multiple runs. 
* **quota_goal:** Reach a set number of quotas to win.
* **monster_hunter:** Win by filming a specific number of unique monsters.
* **hat_collector:** Purchase a configurable number of hats.
* **item_collector** Purchase a configurable number of store items and emotes.


### Check Options
* **quota_requirement:** When enabled, completing a quota grants a randomized item.
*  When disabled, ALL quota-related checks are removed from the pool and the 'quota_goal' Goal option becomes invalid. 
* **include_hats / include_emotes:** Put's checks behind the items in Phil's Hat Shop and the in-game store.
* When include_hats is disabled the 'hat_collector' goal option becomes invalid. When include-emotes is disabled the 'item_collector' goal becomes invalid.
* **sponsorsanity:** Adds extra check locations for completing sponsorship deals.
* **difficult_monsters:** When on, progression items can be hidden behind dangerous monster encounters (like Flicker or Big Slap).

## 🚀 How to Generate
1. Open your `Content Warning.yaml` and set your `name`.
2. Adjust your preferred goals and settings.
3. Place the YAML in your Archipelago `Players` folder along with other player's YAML files.
4. Run the generate command on the Archipelago launcher
5. The output file will be in your outputs folder.
