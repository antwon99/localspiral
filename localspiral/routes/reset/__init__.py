from flask import Blueprint, jsonify, session

reset_bp = Blueprint("reset", __name__)

@reset_bp.route("/reset", methods=["GET"])
def reset_state():
    """Clear any stored game state from the session."""
    session.pop("game_state", None)
    return jsonify({"message": "Game state cleared"})
