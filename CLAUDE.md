# CLAUDE.md — APWorld Project rails

This file is auto-loaded by Claude Code at session start. Read [README.md](README.md) for the user guide.

## What this project is, in one paragraph

The Archipelago world definition (APWorld) for *Content Warning*. This Python package defines item lists, location lists, randomization rules, and generation options. It runs on the Archipelago server and generates randomized Content Warning seeds. The sibling repo [`../cw-archipelago-mod/`](../cw-archipelago-mod/) is the C# mod that runs in-game and applies received items to game state.

## Build & deploy

```
python -m PyInstaller -F -n APClient arcapi.py
# Then the .apworld is generated and placed in the local Archipelago custom_worlds folder
```

For testing locally, you can generate a seed with:
```
python -m worlds generate [path/to/yaml]
```

See the Archipelago development docs for full setup. The `.apworld` file is generated from source during development.

## The two-piece architecture (read this before adding items/locations)

Archipelago needs **both** halves to work:

1. **This repo (cw-apworld, Python)** — APWorld that runs on the server — defines item lists, location lists, randomization rules, and options.
2. **The C# Mod** (in [`../cw-archipelago-mod/`](../cw-archipelago-mod/)) — runs in-game — fires location checks, applies received items, shows UI.

When adding or renaming items/locations here, **the matching change must land in the mod too.** IDs and names must match exactly. The base ID is `98765000`, and each item/location uses a fixed offset from there. See [doc/adding-items-and-locations.md](../cw-archipelago-mod/doc/adding-items-and-locations.md) in the mod repo for the full procedure (it covers both repos).

## Project structure

| File | Purpose |
|------|---------|
| [`items.py`](items.py) | Item definitions: `item_table`, item names, filler/trap items, money pool |
| [`locations.py`](locations.py) | Location definitions: `location_table`, location names, location totals |
| [`regions.py`](regions.py) | Region graph: `CW_regions`, how regions connect |
| [`rules.py`](rules.py) | Access rules: which items unlock which locations (`set_region_rules`, `set_location_rules`) |
| [`options.py`](options.py) | YAML options: toggles, ranges, goals that players can customize |
| [`__init__.py`](__init__.py) | World class: ties everything together, implements `create_regions` and `create_items` |
| [`names/`](names/) | Enums for item/location/region names (used as constants in other files) |

## Key constants & IDs

| Constant | Location | Purpose |
|----------|----------|---------|
| `98765000` | `items.py` (base ID) | Base offset for all item IDs |
| `MONEY_FILLER_POOL` | `items.py` | Standard money filler denominations |
| `_HIGH_VIEW_MILESTONES` | `__init__.py` | View thresholds that get filler when quotas are low |
| `_MULTIPLAYER_ONLY_MONSTERS` | `__init__.py` | Monsters that require multiple players (e.g., Weeping) |

## Common tasks

| Task | Edit | Notes |
|------|------|-------|
| Add a new item | `items.py` + assign ID + mod must add handler | IDs must be sequential from base; see two-piece note above |
| Add a new location | `locations.py` + assign ID + mod must fire check | Same ID/name sync requirement |
| Add an option toggle | `options.py` + reference in `__init__.py` or `rules.py` | Follow existing toggle patterns (e.g., `DefaultOnToggle`) |
| Change generation rules | `__init__.py` (`create_regions`/`create_items`) or `rules.py` | `create_regions` filters locations; `create_items` builds item pool; `set_rules` gates access |
| Adjust item distribution | `__init__.py` (`create_items`) | Manage `ItemClassification.progression` vs `.useful` vs `.filler` |
| Change victory conditions | `rules.py` (`set_rules`) | Implement stacked goals as AND/OR combinations of location checks |

## Common entry points

| Need | Location |
|------|----------|
| Change what locations exist in a world | `__init__.py:create_regions` — filters regions/locations based on options |
| Change what items are in the pool | `__init__.py:create_items` — builds item pool with classification, respects filler pools |
| Change what unlocks what | `rules.py:set_region_rules` / `set_location_rules` — Archipelago's access logic |
| Change YAML options | `options.py` — add/modify option classes; tie them to generation logic in `__init__.py` |
| Read player's option values | `self.options.<OptionName>.value` (inside World class methods) |
| Define win conditions | `rules.py:set_rules` — set the `completion_condition` based on goal toggles |

## Debugging / Testing

- **Generate a test seed locally:** Place a `.yaml` in a test folder and run `python -m worlds generate <folder>`. Check the `.txt` output for errors.
- **Inspect a generated world:** After generation, examine the `.archipelago` file (JSON) to see items placed and rules applied.
- **Common mistakes:** Item/location IDs don't match the mod, option values aren't checked before use, access rules reference non-existent items.

## Logging

Use Python's standard `logging` module. The Archipelago harness will capture and display logs during generation.

```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"[CWWorld] Creating items: {len(self.multiworld.itempool)} total")
```

## When in doubt

- Don't add speculative abstractions or backwards-compat shims. The APWorld is at v0.1; ship simple changes.
- The reference mod [`../cw-reference/`](../cw-reference/cw-reference/) (decompiled CW source + examples) is read-only — use it for game-internals lookups only.
- Check the Archipelago [docs](https://archipelago.gg/docs/) for World API patterns (regions, rules, item classification, etc.).
- Ask the sibling mod repo (via `Closes` in a cross-repo PR) if changes need coordination.
