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
| `VIEW_MILESTONES` | `locations.py` | (day, lifetime_total, quota) per-day view milestones — source of truth for view checks |
| `_DIFFICULT_MONSTERS` | `locations.py` | Monsters whose tier 2/3 are always filler regardless of toggles |
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

## Working with issues

Issues are filed with detailed Actionable Tasks lists, often co-authored with another AI assistant before reaching the repo. Trust the *mechanical* parts (renames, reorders, file moves); expect ambiguity in the *domain* parts — anything where the right answer depends on game-side knowledge or playtest experience the issue author has and you don't.

Before coding:

1. **Read related issues together.** Cross-references like "Following the X refactor…" or shared option/slot-data names mean issues are dependent — implement and merge them in **one PR**. Splitting them lands dead config in `main` between merges and forces the sibling-repo update to happen twice.
2. **Surface ambiguities first via `gh issue comment <num>`.** When a task needs context the issue text doesn't supply, post numbered questions with a/b/c options and a recommended pick. Move on to other workable issues while waiting — do not guess. The issue author is the only person who can answer; comments also create a durable record for whoever (or whichever AI) picks the work up later.
3. **Flag cross-repo coordination.** Slot-data key renames, item/location ID changes, new in-game pickups, and new client events all require matching changes in the sibling repo (apworld ↔ mod). When surfacing questions, call these out so the sibling-repo issue can be filed in the same window and both sides land together.

## Branch hygiene

- One branch per issue, or per issue group bundled into one PR. Names: `fix/issue-N-<slug>`.
- **Don't piggyback unrelated commits.** Drive-by changes on a feature branch invite merge conflicts that have nothing to do with the issue's actual work, and force a force-push to recover.
- Use `Closes #N` (or `Closes Org/Repo#N` for cross-repo) in PR descriptions so issues auto-close on merge.
