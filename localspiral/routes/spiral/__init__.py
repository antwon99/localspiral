from flask import Blueprint, jsonify

from ...utils.spiral_state import spiral_status
from ...utils.state import load_game_state

spiral_bp = Blueprint("spiral", __name__)


@spiral_bp.route("/spiral", methods=["GET"])
def spiral_example():
    """Return current spiral score and sanity level."""
    state = load_game_state()
    score = state.spiral_score
    return jsonify({
        "score": round(score, 3),
        "sanity": state.sanity,
        "status": spiral_status(score),
        "turn": state.turn_count,
    })
