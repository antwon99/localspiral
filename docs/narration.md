# Narration and Turns

Every player prompt triggers `process_turn` which advances the game state. The function performs movement parsing, enemy updates, and zone checks before constructing a system prompt for the OpenAI API.

The system prompt includes Tyler's display name, tone and employer from the loaded character profile. It also lists the current turn number, map descriptions, nearby enemies and the latest hallucination if any. Tyler's response is generated with `generate_reply` and may be distorted based on the spiral score.

After replying, drift scoring compares the prompt and reply (and the previous reply) using `calculate_drift`. This drift, plus trigger and anchor words, updates the spiral. The spiral score also decays slightly on calm turns and influences a `paranoia_level` value that is reported back in the next system prompt.

The text of every reply and prompt is appended to `state.history`. To limit memory, history is truncated to at most the last three pairs.

If sanity reaches zero the frontend locks input and displays the final score.
