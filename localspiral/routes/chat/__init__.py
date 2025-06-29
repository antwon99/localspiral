from flask import Blueprint, request, jsonify

from ...utils import game_state, generate_narration
from ...utils.spiral import update_spiral
from ...utils.map_utils import parse_direction, move_position, render_map

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    prompt = data.get("prompt", "")
    game_state.GAME_STATE.turn += 1

    direction = parse_direction(prompt)
    if direction:
        new_pos, moved = move_position(game_state.GAME_STATE.position, direction, game_state.GAME_STATE.map)
        game_state.GAME_STATE.position = new_pos
        if moved:
            narration = f"Tyler moves {direction}."
        else:
            narration = f"Tyler cannot move {direction}."
    else:
        narration = generate_narration(prompt, game_state.GAME_STATE)

    update_spiral(game_state.GAME_STATE, prompt, narration)
    game_state.GAME_STATE.last_narration = narration
    grid = render_map(game_state.GAME_STATE.map, game_state.GAME_STATE.position)
    return jsonify(
        {
            "turn": game_state.GAME_STATE.turn,
            "response": narration,
            "map": grid,
            "spiral": game_state.GAME_STATE.spiral,
        }
    )
