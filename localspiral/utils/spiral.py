from typing import Iterable

from .game_state import GameState


def update_spiral(game_state: GameState, prompt: str, response: str) -> None:
    """Very simple spiral scoring based on trigger keywords."""
    triggers: Iterable[str] = game_state.character.get("spiral_triggers", [])
    increment = 1
    lower_prompt = prompt.lower()
    lower_response = response.lower()
    for trig in triggers:
        if trig in lower_prompt or trig in lower_response:
            increment += 5
    game_state.spiral = min(100, game_state.spiral + increment)
