# Spiral and Sanity

The spiral score tracks how unstable Tyler's narration has become. It is updated each turn by `process_turn` in `game_loop.py`. Drift between the player's prompt, prior replies, and Tyler's latest response all contribute to the score along with trigger words and anchors.

## Triggers and Anchors

Each character profile may list words that push or stabilize the spiral. If a profile omits triggers, the defaults in `spiral_state.py` are used:

```
shit, fuck, die, death, run, kill, escape
```

Recovery anchors work the same way but reduce drift. Example from `tyler.json`:

```
"spiral_triggers": ["die", "death", "kill", "escape"],
"recovery_anchors": ["coffee", "calm", "Onward"]
```

`check_keywords` counts the occurrences of these words in the current prompt. That count influences the spiral delta.

## Score Calculation

`process_turn` applies several weighted components:

```
drift_component   = (drift_user + drift_history) * DRIFT_WEIGHT
trigger_component = triggers * TRIGGER_WEIGHT
anchor_component  = anchors * ANCHOR_WEIGHT
```

The final delta is capped by `SPIRAL_DRIFT_CAP` and the score decays slightly every turn. See `game_loop.py` lines 247‑269 for the implementation.

Sanity is recalculated via `GameState.update_sanity()`. Starting sanity comes from the character profile and decreases by `20 * spiral_score`.

A spiral score under 2 is **Lucid**, between 2 and 4 is **Questioning**, and 4+ is **Erratic** as defined in `spiral_state.spiral_status`.
