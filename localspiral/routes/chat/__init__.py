from flask import Blueprint, jsonify, request
import logging

from ...utils.map import generate_map
from ...utils.scoring import calculate_drift
from ...utils.spiral_state import (
    analyze_map,
    distort_reply,
    mutate_perceived_grid,
    spiral_status,
    describe_surroundings,
    check_keywords,
)
from ...utils.state import load_game_state, save_game_state

from ...utils.dialogue import generate_reply

chat_bp = Blueprint("chat", __name__)
logger = logging.getLogger(__name__)


@chat_bp.route("/chat", methods=["GET"])
def chat_example():
    """Return a dynamic response influenced by the current game state."""
    prompt = request.args.get("prompt")
    if not prompt:
        return jsonify({"message": "No prompt provided."})

    state = load_game_state()

    spiral_score = state.spiral_score
    seed = state.map_seed
    grid = state.map_grid
    if grid is None:
        grid = generate_map(seed)
        state.map_grid = grid
    perceived = state.perceived_grid
    if perceived is None:
        perceived = [row[:] for row in grid]
    location = state.player_loc
    if 0 <= location[0] < len(grid) and 0 <= location[1] < len(grid[0]):
        grid[location[0]][location[1]] = "@"
    perceived = mutate_perceived_grid(perceived, spiral_score)
    state.perceived_grid = perceived
    analysis = analyze_map(grid)
    perceived_analysis = analyze_map(perceived)
    surroundings = describe_surroundings(perceived, location)
    grid_text = "\n".join("".join(row) for row in perceived)

    status = spiral_status(spiral_score)

    char_data = state.character or {}
    base_prompt = f"You are {char_data.get('display_name', 'Tyler Scienceman')}"
    employer = char_data.get('employer')
    if employer:
        base_prompt += f" employed by {employer}"
    tone = char_data.get('tone')
    if tone:
        base_prompt += f" with a {tone} tone"
    intro = char_data.get('intro_prompt')
    if intro:
        base_prompt += f". {intro}"
    if state.last_hallucination:
        base_prompt += f" Last hallucination: {state.last_hallucination}."
    if state.paranoia_level:
        base_prompt += f" Paranoia level {state.paranoia_level:.2f}."

    system_prompt = (
        base_prompt
        + f"\nCurrent map description: {analysis.get('description')}"
        + f"\nHallucinated map description: {perceived_analysis.get('description')}"
        + f"\nLocation: {location}"
        + f"\nNearby: {surroundings}"
        + f"\nSpiral status: {status} ({spiral_score:.2f})"
        + f"\nMap grid:\n{grid_text}"
    )

    # history alternates: [AI reply, user prompt, AI reply, user prompt, ...]
    history = state.history
    try:
        raw_reply = generate_reply(prompt, system_prompt=system_prompt)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)})

    drift_user = calculate_drift(prompt, raw_reply)
    if len(history) >= 2:
        drift_history = calculate_drift(history[-2], raw_reply)
    else:
        drift_history = 0.0
    trigger_words = None
    if isinstance(state.character, dict):
        trigger_words = state.character.get("spiral_triggers")
    triggers = check_keywords(prompt, trigger_words)
    logger.debug(
        "Drift user=%.3f history=%.3f triggers=%s",
        drift_user,
        drift_history,
        triggers,
    )
    spiral_score += drift_user + drift_history + triggers * 0.5
    if drift_user < 0.2 and drift_history < 0.2 and triggers == 0:
        logger.debug("Drift user=%.3f history=%.3f", drift_user, drift_history)
        spiral_score = max(0.0, spiral_score - 0.05)
        state.paranoia_level = max(0.0, state.paranoia_level - 0.1)
    else:
        state.paranoia_level = min(
            10.0, state.paranoia_level + drift_user + drift_history + triggers * 0.5
        )

    reply, hallucination = distort_reply(raw_reply, spiral_score, return_hallucination=True)
    if hallucination:
        state.last_hallucination = hallucination
    if spiral_score >= 5:
        reply += f" (You perceive {perceived_analysis.get('description')})"

    # keep alternating order: [reply, prompt, ...]
    history.append(raw_reply)
    history.append(prompt)
    state.history = history[-5:]
    state.spiral_score = spiral_score
    state.update_sanity()
    breakdown = state.sanity <= 0
    save_game_state(state)

    state_dict = {
        "spiral_score": round(state.spiral_score, 3),
        "sanity": state.sanity,
        "status": spiral_status(state.spiral_score),
        "map_seed": state.map_seed,
        "location": state.player_loc,
        "description": analysis.get("description"),
        "perceived_description": perceived_analysis.get("description"),
    }
    return jsonify({"message": reply, "state": state_dict, "breakdown": breakdown})
