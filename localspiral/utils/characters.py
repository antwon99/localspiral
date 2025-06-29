import json
from pathlib import Path

CHARACTER_DIR = Path(__file__).resolve().parent.parent / "characters"


def load_character(character_id: str) -> dict:
    """Load a character profile from JSON."""
    path = CHARACTER_DIR / f"{character_id}.json"
    with path.open() as f:
        return json.load(f)
