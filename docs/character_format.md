# Character Format

Each character is defined by a JSON file with the following fields:

- `id`: Unique identifier.
- `display_name`: Name shown to players.
- `starting_sanity`: Initial sanity meter value.
- `spiral_triggers`: Words or actions that accelerate collapse.
- `recovery_anchors`: Phrases that stabilize the character.
- `tone`: Narrative tone used by the AI.
- `intro_prompt`: Starting line for story generation.

See `src/characters/sample_character.json` for an example.
