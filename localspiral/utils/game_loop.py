"""Core game loop helpers."""

from __future__ import annotations

from typing import Tuple
import random

from .map import generate_map, with_entities, clean_entities
from .zones import (
    at_door,
    should_leave_zone,
    move_to_next_zone,
    ensure_zone_map,
    door_visible,
)
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


def extract_direction(text: str) -> str | None:
    """Return the first movement direction found in ``text``."""
    lowered = text.lower()
    for name in _DIRECTION_VECTORS:
        if name in lowered:
            return name
    return None

# thresholds for hallucination effects
HALLUCINATION_SCORE_THRESHOLD = 5
# hallucinations should only appear when sanity is very low
HALLUCINATION_SANITY_THRESHOLD = 25

# scoring configuration
DRIFT_WEIGHT = 0.5  # sensitivity of drift to spiral gain
TRIGGER_WEIGHT = 0.5
ANCHOR_WEIGHT = 1.0
DRIFT_IGNORE_THRESHOLD = 0.3
SPIRAL_DRIFT_CAP = 5


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
        zones = getattr(state, "zones", [])
        index = getattr(state, "zone_index", 0)
        if zones:
            grid = ensure_zone_map(state.map_seed, zones[index], index)
        else:
            grid = generate_map(state.map_seed)
        state.map_grid = grid
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

def advance_state(state: GameState) -> list[list[str]]:
    """Update enemy positions and hallucinated view for the current turn.

    The returned grid includes entity markers and hallucination effects for
    use in narration while ``state.perceived_grid`` stores a clean version.
    """
    grid = state.map_grid
    if grid is None:
        zones = getattr(state, "zones", [])
        index = getattr(state, "zone_index", 0)
        if zones:
            zone = zones[index]
            grid = ensure_zone_map(state.map_seed, zone, index)
        else:
            grid = generate_map(state.map_seed)
        state.map_grid = grid

    if not state.enemies or random.random() < 0.25:
        add_enemy(state)
    if state.turn_count and state.turn_count % 5 == 0:
        add_enemy(state, hallucination=True)
        state.last_hallucination = "A flickering foe looms."

    update_enemies(state)

    enemy_positions = [e.position for e in state.enemies]
    display = with_entities(grid, state.player_loc, enemy_positions)
    score = state.spiral_score
    if not (
        score >= HALLUCINATION_SCORE_THRESHOLD
        and state.sanity <= HALLUCINATION_SANITY_THRESHOLD
    ):
        score = 0.0
    hallucinated = mutate_perceived_grid(display, score)
    state.perceived_grid = clean_entities(hallucinated)
    return hallucinated


def process_turn(prompt: str, state: GameState) -> Tuple[str, GameState, list[list[str]] | None]:
    """Process a single turn of user input.

    Movement commands in ``prompt`` are applied, the assistant reply is
    generated and the spiral score updated. The modified ``GameState`` is
    returned alongside the reply text.
    """

    state.turn_count += 1
    state.chat_count += 1
    lower = prompt.lower()
    zone_message: str | None = None
    current_zone = None
    starting_zone = state.zone_index
    if getattr(state, "zones", None):
        current_zone = state.zones[state.zone_index]
        if should_leave_zone(lower, current_zone):
            zone_message = move_to_next_zone(state)
            if state.zone_index != starting_zone:
                zone_changed = True

    grid = state.map_grid
    if grid is None:
        zones = getattr(state, "zones", [])
        index = getattr(state, "zone_index", 0)
        if zones:
            grid = ensure_zone_map(state.map_seed, zones[index], index)
        else:
            grid = generate_map(state.map_seed)
        state.map_grid = grid

    player_dir = extract_direction(lower)
    if player_dir:
        state.pending_player_dir = player_dir

    trigger_words = None
    anchor_words = None
    if isinstance(state.character, dict):
        trigger_words = state.character.get("spiral_triggers")
        anchor_words = state.character.get("recovery_anchors")

    triggers = check_keywords(prompt, trigger_words)
    anchors = check_keywords(prompt, anchor_words)

    delta_keywords = triggers * TRIGGER_WEIGHT - anchors * ANCHOR_WEIGHT

    drift_prompt = 0.0
    if len(state.history) >= 2:
        drift_prompt = calculate_drift(state.history[-2], prompt)

    early_component = drift_prompt * DRIFT_WEIGHT

    delta_early = 0.0
    if early_component > DRIFT_IGNORE_THRESHOLD:
        delta_early += early_component
    delta_early = max(-SPIRAL_DRIFT_CAP, min(SPIRAL_DRIFT_CAP, delta_early))

    state.spiral_score = max(
        0.0, state.spiral_score + delta_keywords + delta_early
    )
    state.update_sanity()

    def _spammy(text: str) -> bool:
        parts = [p.strip() for p in text.split(",") if p.strip()]
        return len(parts) >= 3 and all(len(p.split()) <= 2 for p in parts)

    spam_warning = _spammy(prompt)

    door_hint: str | None = None
    zone_changed = False
    display_grid: list[list[str]] | None = None
    if at_door(state.map_grid, state.player_loc):
        if (
            current_zone
            and current_zone.name.lower() == "office"
            and state.zone_index == 0
        ):
            zone_message = 'There\u2019s a door here. Type "leave office" to continue.'
        else:
            msg = move_to_next_zone(state)
            if msg:
                zone_message = msg
            if state.zone_index != starting_zone:
                zone_changed = True
    elif current_zone and current_zone.name.lower() == "office" and current_zone.door_loc:
        if door_visible(
            state.map_grid, current_zone.door_loc, state.player_loc, max_range=3
        ):
            dr = abs(current_zone.door_loc[0] - state.player_loc[0])
            dc = abs(current_zone.door_loc[1] - state.player_loc[1])
            if dr + dc <= 3:
                door_hint = "A door is visible nearby."

    if door_hint:
        zone_message = f"{door_hint}\n{zone_message}" if zone_message else door_hint

    grid = state.map_grid
    enemy_positions = [e.position for e in state.enemies]
    display = with_entities(grid, state.player_loc, enemy_positions)
    score = state.spiral_score
    if not (
        score >= HALLUCINATION_SCORE_THRESHOLD
        and state.sanity <= HALLUCINATION_SANITY_THRESHOLD
    ):
        score = 0.0
    hallucinated = mutate_perceived_grid(display, score)
    state.perceived_grid = clean_entities(hallucinated)
    encounter = None
    location = state.player_loc

    analysis = analyze_map(grid)
    perceived_analysis = analyze_map(hallucinated)
    surroundings = describe_surroundings(hallucinated, location)
    location_desc = describe_location(hallucinated, location)
    nearby = [
        e
        for e in state.enemies
        if abs(e.position[0] - location[0]) <= 1
        and abs(e.position[1] - location[1]) <= 1
    ]
    enemy_info = (
        f"{len(nearby)} enemy{'ies' if len(nearby) != 1 else ''} nearby"
        if nearby
        else "no enemies nearby"
    )
    grid_text = "\n".join("".join(row) for row in hallucinated)

    char_data = state.character or {}
    base_prompt = (
        f"You are {char_data.get('display_name', 'Tyler Scienceman')}"
    )
    if current_zone:
        base_prompt += f" currently in {current_zone.name}"
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

    system_prompt = (
        base_prompt
        + f"\nTurn: {state.turn_count}"
        + move_line
        + f"\nCurrent map description: {analysis.get('description')}"
        + "\nHallucinated map description: "
        + perceived_analysis.get('description')
        + f"\nLocation: {location}"
        + f"\nOn this tile: {location_desc}"
        + f"\nNearby: {surroundings}"
        + f"\n{enemy_info}"
        + (f"\nEncounter: {encounter}" if encounter else "")
        + f"\nSpiral status: {spiral_status(state.spiral_score)}"
        + f" ({state.spiral_score:.2f})"
        + f"\nMap grid:\n{grid_text}"
    )

    raw_reply = generate_reply(prompt, system_prompt=system_prompt)
    if spam_warning:
        raw_reply = "Why are you just listing words at me?"
        if zone_message:
            raw_reply = f"{zone_message}\n" + raw_reply
    elif zone_message:
        raw_reply = f"{zone_message}\n" + raw_reply

    drift_user = calculate_drift(prompt, raw_reply)
    if len(state.history) >= 2:
        drift_history = calculate_drift(state.history[-2], raw_reply)
    else:
        drift_history = 0.0

    spiral_score = state.spiral_score

    drift_component = (drift_user + drift_history) * DRIFT_WEIGHT
    trigger_component = triggers * TRIGGER_WEIGHT
    anchor_component = anchors * ANCHOR_WEIGHT

    delta = 0.0
    if drift_component > DRIFT_IGNORE_THRESHOLD:
        delta += drift_component
    delta = max(-SPIRAL_DRIFT_CAP, min(SPIRAL_DRIFT_CAP, delta))

    spiral_score = max(0.0, spiral_score + delta - 0.02)

    if (
        drift_user < DRIFT_IGNORE_THRESHOLD
        and drift_history < DRIFT_IGNORE_THRESHOLD
        and triggers == 0
        and anchors == 0
    ):
        spiral_score = max(0.0, spiral_score - 0.05)
        state.paranoia_level = max(0.0, state.paranoia_level - 0.1)

    state.spiral_score = spiral_score
    state.update_sanity()

    paranoia_change = (
        drift_component + trigger_component - anchors * 0.2 + 0.05
    )
    state.paranoia_level = max(
        0.0, min(10.0, state.paranoia_level + paranoia_change)
    )

    if (
        spiral_score >= HALLUCINATION_SCORE_THRESHOLD
        and state.sanity <= HALLUCINATION_SANITY_THRESHOLD
    ):
        score_for_text = spiral_score
    else:
        score_for_text = 0.0

    reply, hallucination = distort_reply(
        raw_reply, score_for_text, return_hallucination=True
    )
    if hallucination:
        state.last_hallucination = hallucination
    if score_for_text >= HALLUCINATION_SCORE_THRESHOLD:
        reply += f" (You perceive {perceived_analysis.get('description')})"

    tyler_dir = extract_direction(reply)
    if tyler_dir:
        state.pending_tyler_dir = tyler_dir

    decision_ready = False
    if state.pending_player_dir and state.pending_tyler_dir:
        decision_ready = True
    elif state.chat_count >= 5:
        decision_ready = True

    move_result = None
    encounter = None
    if decision_ready:
        agree = (
            state.pending_player_dir
            and state.pending_player_dir == state.pending_tyler_dir
        )
        if agree:
            moved = apply_move(state, state.pending_player_dir)
            if moved and at_door(state.map_grid, state.player_loc):
                msg = move_to_next_zone(state)
                if msg:
                    zone_message = msg if not zone_message else f"{zone_message}\n{msg}"
                if state.zone_index != starting_zone:
                    zone_changed = True
            move_result = (
                f"Tyler moves {state.pending_player_dir}."
                if moved
                else f"Tyler tries to move {state.pending_player_dir} but is blocked."
            )
        else:
            move_result = "Tyler hesitates, unsure which way to go."
        display = advance_state(state)
        encounter = handle_enemy_encounters(state)
        display_grid = with_entities(state.map_grid, state.player_loc, [e.position for e in state.enemies])
        state.chat_count = 0
        state.pending_player_dir = None
        state.pending_tyler_dir = None
        grid_text = "\n".join("".join(row) for row in display)
        perceived_analysis = analyze_map(display)
        if move_result:
            reply += "\n" + move_result
        if encounter:
            reply += f" {encounter}"
        if zone_message:
            reply = f"{zone_message}\n" + reply

    history = state.history
    history.append(raw_reply)
    history.append(prompt)
    # Remove oldest entries in prompt/reply pairs to keep history length even
    while len(history) > 6:
        history.pop(0)
        history.pop(0)
    state.history = history

    if state.zone_index != starting_zone:
        zone_changed = True

    if display_grid is None and zone_changed:
        display_grid = with_entities(
            state.map_grid, state.player_loc, [e.position for e in state.enemies]
        )

    return reply, state, display_grid
