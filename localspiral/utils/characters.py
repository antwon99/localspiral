"""Utilities for loading character profiles."""

import json

REQUIRED_FIELDS = {
    "id",
    "display_name",
    "starting_sanity",
    "spiral_triggers",
    "recovery_anchors",
    "tone",
    "intro_prompt",
}


def load_character(path: str) -> dict:
    """Load and validate a character JSON file.

    Parameters
    ----------
    path:
        Path to the JSON file containing the character definition.

    Returns
    -------
    dict
        Dictionary representing the character profile.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If required fields are missing or the JSON is malformed.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(
            f"Character file {path} missing fields: {missing_list}"
        )

    return data
