"""Helpers for generating narration text.

This module interfaces with OpenAI to craft Tyler Scienceman's responses. When
OpenAI is unavailable, a deterministic placeholder is used so the rest of the
system remains testable.
"""

from __future__ import annotations

import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - openai may not be installed
    openai = None

from .game_state import GameState


DEFAULT_MODEL = "gpt-3.5-turbo"


def _call_openai(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL) -> str:
    """Return OpenAI chat completion or raise."""
    if openai is None or os.getenv("OPENAI_API_KEY") is None:
        raise RuntimeError("OpenAI not available")

    response = openai.ChatCompletion.create(model=model, messages=messages)
    content = response["choices"][0]["message"]["content"].strip()
    return content


def generate_narration(prompt: str, state: GameState) -> str:
    """Generate Tyler's narration based on the prompt and current state."""
    character = state.character
    system_msg = (
        f"You are {character.get('display_name', 'Tyler')} speaking in a "
        f"{character.get('tone', 'dry')} tone. Respond narratively to the player's "
        "prompt while referencing your spiral state and memories."
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt},
    ]

    try:
        return _call_openai(messages)
    except Exception:
        # Fallback placeholder used in tests or when API isn't reachable.
        sanitized = prompt.strip()
        if not sanitized:
            return f"{character.get('display_name', 'Tyler')} hesitates, saying nothing."
        return (
            f"{character.get('display_name', 'Tyler')} ponders '{sanitized}' "
            "and mutters about spirals."
        )

