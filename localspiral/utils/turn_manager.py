"""Central turn management functions."""

from __future__ import annotations

from typing import Any, Dict

from .state import load_game_state, save_game_state, GameState
from .game_loop import process_turn
from .spiral_state import (
    analyze_map,
    spiral_status,
    get_available_directions,
)
from .map import with_entities


def _compile_state_response(state: GameState) -> Dict[str, Any]:
    """Create a serialisable snapshot of ``state`` for API responses."""
    analysis = analyze_map(state.map_grid or [])
    perceived_analysis = analyze_map(state.perceived_grid or [])
    directions = get_available_directions(state.map_grid or [], state.player_loc)

    return {
        "spiral_score": round(state.spiral_score, 3),
        "sanity": state.sanity,
        "status": spiral_status(state.spiral_score),
        "turn": state.turn_count,
        "map_seed": state.map_seed,
        "location": state.player_loc,
        "description": analysis.get("description"),
        "perceived_description": perceived_analysis.get("description"),
        "directions": directions,
        "chat_count": state.chat_count,
    }


def run_turn(user_input: str) -> Dict[str, Any]:
    """Execute a full game turn from ``user_input``.

    This loads the saved :class:`GameState`, applies ``process_turn`` and
    returns the structured response for the `/chat` endpoint.
    """
    state = load_game_state()

    reply: str
    grid_update: list[list[str]] | None
    reply, state, grid_update = process_turn(user_input, state)
    save_game_state(state)

    enemy_positions = [e.position for e in state.enemies]
    real_grid = with_entities(state.map_grid or [], state.player_loc, enemy_positions)
    perceived_grid = state.perceived_grid or []

    char_name = None
    if isinstance(state.character, dict):
        char_name = state.character.get("display_name")
    zone_name = None
    if getattr(state, "zones", None):
        zone_name = state.zones[state.zone_index].name

    response: Dict[str, Any] = {
        "message": reply,
        "state": _compile_state_response(state),
        "breakdown": state.sanity <= 0,
        "debug": {
            "perceived_grid": perceived_grid,
            "real_grid": real_grid,
            "enemies": enemy_positions,
        },
    }

    if grid_update is not None:
        response["grid"] = {
            "seed": state.map_seed,
            "grid": grid_update,
            "analysis": analyze_map(state.map_grid or []),
            "location": state.player_loc,
            "display_name": char_name,
            "zone": zone_name,
        }

    return response
