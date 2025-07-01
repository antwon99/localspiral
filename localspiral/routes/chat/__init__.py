from flask import Blueprint, jsonify, request
import logging

from ...utils.turn_manager import run_turn

chat_bp = Blueprint("chat", __name__)
logger = logging.getLogger(__name__)


@chat_bp.route("/chat", methods=["GET"])
def chat_example():
    """Return a dynamic response influenced by the current game state."""
    prompt = request.args.get("prompt")
    if not prompt:
        return jsonify({"message": "No prompt provided."})

    try:
        response = run_turn(prompt)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)})

    return jsonify(response)
