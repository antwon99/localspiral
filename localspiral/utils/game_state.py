from __future__ import annotations

from typing import Dict

from .characters import load_character
from .map_utils import generate_map


class GameState:
    def __init__(self) -> None:
        self.character = load_character("tyler")
        self.map = generate_map()
        self.spiral = 0
        self.turn = 0
        self.position = (len(self.map) // 2, len(self.map[0]) // 2)
        self.last_narration = self.character.get("intro_prompt", "")
        self.hallucinating = False


GAME_STATE = GameState()


def reset_game_state() -> None:
    global GAME_STATE
    GAME_STATE = GameState()
