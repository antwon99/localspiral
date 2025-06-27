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
