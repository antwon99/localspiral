from flask import Blueprint, jsonify, session

from ...utils.spiral_state import spiral_status

spiral_bp = Blueprint("spiral", __name__)


@spiral_bp.route("/spiral", methods=["GET"])
def spiral_example():
    """Return current spiral score and sanity level."""
    score = session.get("spiral_score", 0.0)
    sanity = max(0, 100 - int(score * 20))
    return jsonify({
        "score": round(score, 3),
        "sanity": sanity,
        "status": spiral_status(score),
    })
