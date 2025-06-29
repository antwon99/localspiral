from flask import Blueprint, jsonify

from ...utils import game_state

sanity_bp = Blueprint("sanity", __name__)


@sanity_bp.route("/sanity", methods=["GET"])
def sanity():
    return jsonify({"sanity": game_state.GAME_STATE.sanity})
