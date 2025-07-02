from flask import Blueprint, jsonify

from ...utils.state import load_game_state, save_game_state
from ...utils.turn_manager import _compile_state_response

skip_bp = Blueprint("skip", __name__)

@skip_bp.route("/skip", methods=["GET"])
def skip_chat():
    """Force the chat counter to the movement phase."""
    state = load_game_state()
    if state.chat_count < 5:
        state.chat_count = 5
    save_game_state(state)
    return jsonify({"message": "Ready to move", "state": _compile_state_response(state)})

