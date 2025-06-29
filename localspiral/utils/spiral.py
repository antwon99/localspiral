from typing import Iterable, List

from .game_state import GameState


def update_spiral(game_state: GameState, prompt: str, response: str) -> None:
    """Update spiral score and adjust tone/hallucination state.

    Spiral increases when trigger keywords appear in either the prompt or
    the resulting narration. Crossing configured thresholds alters Tyler's
    tone and eventually marks him as hallucinating.
    """

    triggers: Iterable[str] = game_state.character.get("spiral_triggers", [])
    increment = 1
    lower_prompt = prompt.lower()
    lower_response = response.lower()
    for trig in triggers:
        if trig in lower_prompt or trig in lower_response:
            increment += 5

    game_state.spiral = min(100, game_state.spiral + increment)

    thresholds: List[int] = sorted(game_state.character.get("spiral_thresholds", []))
    tones: List[str] = game_state.character.get(
        "tone_progression", [game_state.character.get("tone", "")]
    )
    stage = 0
    for idx, point in enumerate(thresholds):
        if game_state.spiral >= point:
            stage = min(idx + 1, len(tones) - 1)

    if stage < len(tones):
        game_state.character["tone"] = tones[stage]

    if thresholds and game_state.spiral >= thresholds[-1]:
        game_state.hallucinating = True
    else:
        game_state.hallucinating = False
