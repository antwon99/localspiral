from flask import Blueprint, jsonify, request, session

from ...utils.map import generate_map
from ...utils.scoring import calculate_drift
from ...utils.spiral_state import (
    analyze_map,
    distort_reply,
    spiral_status,
    describe_surroundings,
    check_keywords,
)

from ...utils.dialogue import generate_reply


SYSTEM_PROMPT = "You are Tyler Scienceman, a helpful scientist with a stoic tone."

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["GET"])
def chat_example():
    """Return a dynamic response influenced by the current game state."""
    prompt = request.args.get("prompt")
    if not prompt:
        return jsonify({"message": "No prompt provided."})

    spiral_score = session.get("spiral_score", 0.0)
    seed = session.get("map_seed", 0)
    grid = session.get("map_grid")
    if grid is None:
        grid = generate_map(seed)
        session["map_grid"] = grid
    location = session.get("player_loc", (5, 5))
    if 0 <= location[0] < len(grid) and 0 <= location[1] < len(grid[0]):
        grid[location[0]][location[1]] = "@"
    analysis = session.get("map_analysis", analyze_map(grid))
    surroundings = describe_surroundings(grid, location)
    grid_text = "\n".join("".join(row) for row in grid)

    status = spiral_status(spiral_score)

    system_prompt = (
        SYSTEM_PROMPT
        + f"\nCurrent map description: {analysis.get('description')}"
        + f"\nLocation: {location}"
        + f"\nNearby: {surroundings}"
        + f"\nSpiral status: {status} ({spiral_score:.2f})"
        + f"\nMap grid:\n{grid_text}"
    )

    history = session.get("history", [])
    try:
        raw_reply = generate_reply(prompt, system_prompt=system_prompt)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)})

    drift_user = calculate_drift(prompt, raw_reply)
    drift_history = calculate_drift(history[-1], raw_reply) if history else 0.0
    triggers = check_keywords(prompt)
    print(
        f"Drift user={drift_user:.3f} history={drift_history:.3f} triggers={triggers}"
    )
    spiral_score += drift_user + drift_history + triggers * 0.5
    if drift_user < 0.2 and drift_history < 0.2 and triggers == 0:
        spiral_score = max(0.0, spiral_score - 0.1)

    reply = distort_reply(raw_reply, spiral_score)

    history.append(raw_reply)
    session["history"] = history[-5:]
    session["spiral_score"] = spiral_score

    state = {
        "spiral_score": round(spiral_score, 3),
        "sanity": max(0, 100 - int(spiral_score * 20)),
        "status": spiral_status(spiral_score),
        "map_seed": seed,
        "location": location,
        "description": analysis.get("description"),
    }

    return jsonify({"message": reply, "state": state})
