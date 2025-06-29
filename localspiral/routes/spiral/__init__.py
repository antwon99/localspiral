from flask import Blueprint, jsonify

from ...utils import game_state

spiral_bp = Blueprint("spiral", __name__)


@spiral_bp.route("/spiral", methods=["GET"])
def spiral():
    return jsonify({"spiral": game_state.GAME_STATE.spiral})
