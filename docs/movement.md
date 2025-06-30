# Movement and Map Generation

Maps are deterministic 10x10 grids of `.` and `#` tiles produced by `generate_map` in `utils/map.py`. Passing the same seed always returns the same layout. The helper `compute_seed` converts strings to integer seeds so zone names can influence the result.

`GameState.map_seed` stores the current seed. The `/map` endpoint or `process_turn` will create a map when none exists. Enemies are spawned into open tiles as the game advances.

## Zones

Zones are ordered areas that Tyler travels through. Each `Zone` defines a `door_loc` and `start_loc`. When Tyler reaches a door tile (`D`) or a prompt contains phrases like "leave zone" the next zone is loaded using `ensure_zone_map`. The new map is generated using a seed derived from the base seed and zone index.

```
seed = get_zone_seed(base_seed, zone, index)
```

Tyler's position resets to the zone's `start_loc` when transitioning.

## Moving the Player

Commands containing `north`, `south`, `east` or `west` attempt to move Tyler via `apply_move`. Movement is blocked by walls (`#`) or map boundaries. After each successful move the current turn count increases and the game checks whether Tyler has stepped on a door to trigger a zone change.
