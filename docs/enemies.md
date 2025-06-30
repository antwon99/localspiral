# Enemies

Enemies are simple objects with a position and behaviour flags. They can move randomly, chase Tyler when `aggressive=True`, or follow a patrol route. Hallucinated enemies are marked with `hallucination=True` and increase the spiral score more when encountered.

`advance_state` spawns an enemy when none exist and has a 25% chance to add another each turn. Every five turns a hallucinated enemy appears. `update_enemies` moves each one step according to its behaviour. If Tyler collides with an enemy the spiral score increases by `1.0` (`1.5` for hallucinations). Being adjacent adds `0.5` instead. Descriptive snippets from `handle_enemy_encounters` feed back into the narration.
