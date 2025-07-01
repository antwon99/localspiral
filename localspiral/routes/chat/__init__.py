from flask import Blueprint, jsonify, request
import logging

from ...utils.spiral_state import (
    analyze_map,
    spiral_status,
    get_available_directions,
)
from ...utils.map import with_entities
from ...utils.state import load_game_state, save_game_state
from ...utils.game_loop import process_turn

chat_bp = Blueprint("chat", __name__)
logger = logging.getLogger(__name__)


@chat_bp.route("/chat", methods=["GET"])
def chat_example():
    """Return a dynamic response influenced by the current game state."""
    prompt = request.args.get("prompt")
    if not prompt:
        return jsonify({"message": "No prompt provided."})

    state = load_game_state()

    try:
        reply, state, grid_update = process_turn(prompt, state)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)})

    save_game_state(state)

    analysis = analyze_map(state.map_grid or [])
    perceived_analysis = analyze_map(state.perceived_grid or [])
    breakdown = state.sanity <= 0

    directions = get_available_directions(
        state.map_grid or [], state.player_loc
    )

    enemy_positions = [e.position for e in state.enemies]
    real_grid = with_entities(state.map_grid or [], state.player_loc, enemy_positions)
    perceived_grid = state.perceived_grid or []
    char_name = None
    if isinstance(state.character, dict):
        char_name = state.character.get("display_name")
    zone_name = None
    if getattr(state, "zones", None):
        zone_name = state.zones[state.zone_index].name

    state_dict = {
        "spiral_score": round(state.spiral_score, 3),
        "sanity": state.sanity,
        "status": spiral_status(state.spiral_score),
        "turn": state.turn_count,
        "map_seed": state.map_seed,
        "location": state.player_loc,
        "description": analysis.get("description"),
        "perceived_description": perceived_analysis.get("description"),
        "directions": directions,
    }
    debug = {
        "perceived_grid": perceived_grid,
        "real_grid": real_grid,
        "enemies": enemy_positions,
    }

    response = {
        "message": reply,
        "state": state_dict,
        "breakdown": breakdown,
        "debug": debug,
    }

    if grid_update is not None:
        response["grid"] = {
            "seed": state.map_seed,
            "grid": grid_update,
            "analysis": analysis,
            "location": state.player_loc,
            "display_name": char_name,
            "zone": zone_name,
        }

    return jsonify(response)
