# Character Format

Each character is defined by a JSON file with the following fields:

- `id`: Unique identifier.
- `display_name`: Name shown to players.
- `starting_sanity`: Initial sanity meter value.
- `spiral_triggers`: Words or actions that accelerate collapse.
- `recovery_anchors`: Phrases that stabilize the character.
- `tone`: Narrative tone used by the AI.
- `intro_prompt`: Starting line for story generation.

See `localspiral/characters/sample_character.json` for an example.

## Loading Characters

Use `load_character` from `localspiral/utils/characters.py` to read a profile file::

    from localspiral.utils.characters import load_character

    character = load_character("path/to/profile.json")

The loader checks that all required fields exist and raises `ValueError` if the
file is missing information or is not valid JSON.

## Spiral Weights and Sanity

The spiral score represents how unstable the protagonist is. The constants
`DRIFT_WEIGHT`, `TRIGGER_WEIGHT`, `ANCHOR_WEIGHT`, `DRIFT_IGNORE_THRESHOLD` and
`SPIRAL_DRIFT_CAP` in `localspiral/utils/game_loop.py` tune how much each turn
changes this score. The high level formula, used in `process_turn`, is:

```
drift_component   = (drift_user + drift_history) * DRIFT_WEIGHT
trigger_component = triggers * TRIGGER_WEIGHT
anchor_component  = anchors * ANCHOR_WEIGHT

delta = 0.0
if drift_component > DRIFT_IGNORE_THRESHOLD or trigger_component:
    delta += drift_component + trigger_component
delta -= anchor_component
delta = max(-SPIRAL_DRIFT_CAP, min(SPIRAL_DRIFT_CAP, delta))
spiral_score = max(0.0, spiral_score + delta - 0.02)
```

`process_turn` stores the resulting value in `GameState.spiral_score` and then
calls `GameState.update_sanity` to recompute the sanity meter. `update_sanity`
calculates sanity as the character's starting value minus `20 * spiral_score`.
When the spiral climbs, sanity drops accordingly.

## Extending the Cast

Adding a new protagonist is as simple as creating another JSON file in `localspiral/characters/`. Use the same fields shown above. Unique trigger words and recovery anchors let each character spiral in their own way. Zones are loaded by `get_zones_for_character(id)` in `utils/zones.py`, so providing a matching list there will place the new character in a custom world sequence.
