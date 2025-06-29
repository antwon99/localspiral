from flask import Blueprint, jsonify

from ..utils.game_state import GAME_STATE, reset_game_state


game_bp = Blueprint("game", __name__)


@game_bp.route("/map", methods=["GET"])
def map_route():
    return jsonify({"map": GAME_STATE.map})


@game_bp.route("/reset", methods=["POST"])
def reset_route():
    reset_game_state()
    return jsonify({"status": "reset"})
