from flask import Blueprint, request, jsonify

from ...utils.game_state import GAME_STATE
from ...utils.spiral import update_spiral

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")
    GAME_STATE.turn += 1
    # Placeholder response
    response = f"Tyler hears: {prompt}"
    update_spiral(vars(GAME_STATE), prompt, response)
    return jsonify({"turn": GAME_STATE.turn, "response": response})
