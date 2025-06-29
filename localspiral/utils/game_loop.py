"""Core game loop helpers."""

from __future__ import annotations

from typing import Tuple

from .map import generate_map, with_entities
from .dialogue import generate_reply
from .scoring import calculate_drift
from .spiral_state import (
    analyze_map,
    mutate_perceived_grid,
    describe_surroundings,
    describe_location,
    distort_reply,
    spiral_status,
    check_keywords,
)
from .state import GameState
from .enemies import update_enemies, add_enemy, handle_enemy_encounters


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


def _clean_entities(grid: list[list[str]]) -> list[list[str]]:
    """Return ``grid`` with any entity markers replaced by dots."""
    return [[cell if cell not in {'@', 'X'} else '.' for cell in row] for row in grid]


def advance_state(state: GameState) -> list[list[str]]:
    """Update enemy positions and hallucinated view for the current turn.

    The returned grid includes entity markers and hallucination effects for
    use in narration while ``state.perceived_grid`` stores a clean version.
    """
    grid = state.map_grid
    if grid is None:
        grid = generate_map(state.map_seed)
        state.map_grid = grid

    if not state.enemies:
        add_enemy(state)

    update_enemies(state)

    enemy_positions = [e.position for e in state.enemies]
    display = with_entities(grid, state.player_loc, enemy_positions)
    hallucinated = mutate_perceived_grid(display, state.spiral_score)
    state.perceived_grid = _clean_entities(hallucinated)
    return hallucinated


def process_turn(prompt: str, state: GameState) -> Tuple[str, GameState]:
    """Process a single turn of user input.

    Movement commands contained in ``prompt`` are applied, the assistant reply is
    generated and the spiral score updated. The modified ``GameState`` is
    returned alongside the reply text.
    """

    state.turn_count += 1
    lower = prompt.lower()
    movement_dir: str | None = None
    movement_success = False
    for direction in _DIRECTION_VECTORS:
        if direction in lower:
            movement_dir = direction
            movement_success = apply_move(state, direction)
            break

    display = advance_state(state)
    encounter = handle_enemy_encounters(state)
    grid = state.map_grid
    location = state.player_loc

    analysis = analyze_map(grid)
    perceived_analysis = analyze_map(display)
    surroundings = describe_surroundings(display, location)
    location_desc = describe_location(display, location)
    nearby = [e for e in state.enemies if abs(e.position[0]-location[0]) <= 1 and abs(e.position[1]-location[1]) <= 1]
    enemy_info = f"{len(nearby)} enemy{'ies' if len(nearby)!=1 else ''} nearby" if nearby else "no enemies nearby"
    grid_text = "\n".join("".join(row) for row in display)

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

    move_line = ""
    if movement_dir:
        outcome = "succeeded" if movement_success else "blocked"
        move_line = f"\nMovement attempt: {movement_dir} ({outcome})"

    system_prompt = (
        base_prompt
        + f"\nTurn: {state.turn_count}"
        + move_line
        + f"\nCurrent map description: {analysis.get('description')}"
        + f"\nHallucinated map description: {perceived_analysis.get('description')}"
        + f"\nLocation: {location}"
        + f"\nOn this tile: {location_desc}"
        + f"\nNearby: {surroundings}"
        + f"\n{enemy_info}"
        + (f"\nEncounter: {encounter}" if encounter else "")
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
    anchor_words = None
    if isinstance(state.character, dict):
        trigger_words = state.character.get("spiral_triggers")
        anchor_words = state.character.get("recovery_anchors")

    triggers = check_keywords(prompt, trigger_words)
    anchors = check_keywords(prompt, anchor_words)

    spiral_score = state.spiral_score
    spiral_score += drift_user + drift_history + triggers * 0.5
    spiral_score -= anchors * 0.5
    spiral_score = max(0.0, spiral_score)

    paranoia_change = drift_user + drift_history + triggers * 0.5 - anchors * 0.2
    state.paranoia_level = max(0.0, min(10.0, state.paranoia_level + paranoia_change))

    if drift_user < 0.2 and drift_history < 0.2 and triggers == 0 and anchors == 0:
        spiral_score = max(0.0, spiral_score - 0.05)
        state.paranoia_level = max(0.0, state.paranoia_level - 0.1)

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

