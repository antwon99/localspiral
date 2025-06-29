from flask import Blueprint, jsonify

from ...utils.game_state import GAME_STATE

spiral_bp = Blueprint("spiral", __name__)


@spiral_bp.route("/spiral", methods=["GET"])
def spiral():
    return jsonify({"spiral": GAME_STATE.spiral})
