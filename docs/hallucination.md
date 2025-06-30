# Hallucinations

Hallucinations distort both the map and Tyler's narration once the spiral grows too high. The key thresholds are defined in `game_loop.py`:

```
HALLUCINATION_SCORE_THRESHOLD = 5
HALLUCINATION_SANITY_THRESHOLD = 25
```

Only when the spiral score is 5 or more **and** sanity is 25 or less do visual glitches start appearing. `advance_state` mutates the perceived grid with `mutate_perceived_grid` which replaces random tiles with `?` based on the score. The unmodified grid is kept in `map_grid` for logic while `perceived_grid` stores the hallucinated view.

Tyler's replies are distorted by `distort_reply` in `spiral_state.py`. Different ranges add stronger effects:

- **≥2** – appends "... I think." to the text.
- **≥4** – inserts "I think I saw" fragments.
- **≥5** – two hallucination phrases are injected and the reply is uppercased.
- **≥6** – a single hallucination phrase in all caps.
- **≥8** – maximal distortion plus a "map warping" note.

Whenever `distort_reply` returns a hallucination string it is stored as `state.last_hallucination` and passed back into the next system prompt so Tyler references what he saw.
