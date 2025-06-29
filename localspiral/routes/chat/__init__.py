from flask import Blueprint, jsonify, request
import logging

from ...utils.spiral_state import analyze_map, spiral_status
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
        reply, state = process_turn(prompt, state)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)})

    save_game_state(state)

    analysis = analyze_map(state.map_grid or [])
    perceived_analysis = analyze_map(state.perceived_grid or [])
    breakdown = state.sanity <= 0

    state_dict = {
        "spiral_score": round(state.spiral_score, 3),
        "sanity": state.sanity,
        "status": spiral_status(state.spiral_score),
        "map_seed": state.map_seed,
        "location": state.player_loc,
        "description": analysis.get("description"),
        "perceived_description": perceived_analysis.get("description"),
    }
    return jsonify({"message": reply, "state": state_dict, "breakdown": breakdown})
