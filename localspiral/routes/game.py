from flask import Blueprint, jsonify

from ..utils import game_state
from ..utils.game_state import reset_game_state
from ..utils.map_utils import render_map


game_bp = Blueprint("game", __name__)


@game_bp.route("/map", methods=["GET"])
def map_route():
    grid = render_map(game_state.GAME_STATE.map, game_state.GAME_STATE.position)
    return jsonify({"map": grid})


@game_bp.route("/reset", methods=["POST"])
def reset_route():
    reset_game_state()
    grid = render_map(game_state.GAME_STATE.map, game_state.GAME_STATE.position)
    return jsonify({"status": "reset", "map": grid, "spiral": game_state.GAME_STATE.spiral})
