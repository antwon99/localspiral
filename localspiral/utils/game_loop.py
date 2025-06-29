"""Core game loop helpers."""

from __future__ import annotations

from typing import Tuple

from .map import generate_map
from .dialogue import generate_reply
from .scoring import calculate_drift
from .spiral_state import (
    analyze_map,
    mutate_perceived_grid,
    describe_surroundings,
    distort_reply,
    spiral_status,
    check_keywords,
)
from .state import GameState


_DIRECTION_VECTORS = {
    "north": (-1, 0),
    "south": (1, 0),
    "west": (0, -1),
    "east": (0, 1),
}


def apply_move(state: GameState, direction: str) -> bool:
    """Move the player in ``direction`` if possible.

    Parameters
    ----------
    state:
        The current :class:`GameState`.
    direction:
        One of ``"north"``, ``"south"``, ``"east"`` or ``"west"``.

    Returns
    -------
    bool
        ``True`` if the player moved successfully, ``False`` otherwise.
    """
    grid = state.map_grid
    if grid is None:
        return False

    delta = _DIRECTION_VECTORS.get(direction.lower())
    if delta is None:
        return False

    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    r = state.player_loc[0] + delta[0]
    c = state.player_loc[1] + delta[1]

    if not (0 <= r < rows and 0 <= c < cols):
        return False
    if grid[r][c] == "#":
        return False

    state.player_loc = (r, c)
    return True


def process_turn(prompt: str, state: GameState) -> Tuple[str, GameState]:
    """Process a single turn of user input.

    Movement commands contained in ``prompt`` are applied, the assistant reply is
    generated and the spiral score updated. The modified ``GameState`` is
    returned alongside the reply text.
    """

    lower = prompt.lower()
    for direction in _DIRECTION_VECTORS:
        if direction in lower:
            apply_move(state, direction)
            break

    grid = state.map_grid
    if grid is None:
        grid = generate_map(state.map_seed)
        state.map_grid = grid

    location = state.player_loc
    if 0 <= location[0] < len(grid) and 0 <= location[1] < len(grid[0]):
        grid[location[0]][location[1]] = "@"

    perceived = state.perceived_grid
    if perceived is None:
        perceived = [row[:] for row in grid]
    perceived = mutate_perceived_grid(perceived, state.spiral_score)
    state.perceived_grid = perceived

    analysis = analyze_map(grid)
    perceived_analysis = analyze_map(perceived)
    surroundings = describe_surroundings(perceived, location)
    grid_text = "\n".join("".join(row) for row in perceived)

    char_data = state.character or {}
    base_prompt = f"You are {char_data.get('display_name', 'Tyler Scienceman')}"
    employer = char_data.get("employer")
    if employer:
        base_prompt += f" employed by {employer}"
    tone = char_data.get("tone")
    if tone:
        base_prompt += f" with a {tone} tone"
    intro = char_data.get("intro_prompt")
    if intro:
        base_prompt += f". {intro}"
    if state.last_hallucination:
        base_prompt += f" Last hallucination: {state.last_hallucination}."
    if state.paranoia_level:
        base_prompt += f" Paranoia level {state.paranoia_level:.2f}."

    system_prompt = (
        base_prompt
        + f"\nCurrent map description: {analysis.get('description')}"
        + f"\nHallucinated map description: {perceived_analysis.get('description')}"
        + f"\nLocation: {location}"
        + f"\nNearby: {surroundings}"
        + f"\nSpiral status: {spiral_status(state.spiral_score)} ({state.spiral_score:.2f})"
        + f"\nMap grid:\n{grid_text}"
    )

    raw_reply = generate_reply(prompt, system_prompt=system_prompt)

    drift_user = calculate_drift(prompt, raw_reply)
    if len(state.history) >= 2:
        drift_history = calculate_drift(state.history[-2], raw_reply)
    else:
        drift_history = 0.0

    trigger_words = None
    if isinstance(state.character, dict):
        trigger_words = state.character.get("spiral_triggers")
    triggers = check_keywords(prompt, trigger_words)

    spiral_score = state.spiral_score
    spiral_score += drift_user + drift_history + triggers * 0.5
    if drift_user < 0.2 and drift_history < 0.2 and triggers == 0:
        spiral_score = max(0.0, spiral_score - 0.05)
        state.paranoia_level = max(0.0, state.paranoia_level - 0.1)
    else:
        state.paranoia_level = min(10.0, state.paranoia_level + drift_user + drift_history + triggers * 0.5)

    reply, hallucination = distort_reply(raw_reply, spiral_score, return_hallucination=True)
    if hallucination:
        state.last_hallucination = hallucination
    if spiral_score >= 5:
        reply += f" (You perceive {perceived_analysis.get('description')})"

    history = state.history
    history.append(raw_reply)
    history.append(prompt)
    state.history = history[-5:]
    state.spiral_score = spiral_score
    state.update_sanity()

    return reply, state

