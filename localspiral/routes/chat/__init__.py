from flask import Blueprint, jsonify, request, session

from ...utils.map import generate_map
from ...utils.scoring import calculate_drift

from ...utils.dialogue import generate_reply

SYSTEM_PROMPT = (
    "You are Tyler Scienceman, a helpful scientist with a stoic tone."
)

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['GET'])
def chat_example():
    """Return a dynamic response influenced by the current game state."""
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({'message': 'No prompt provided.'})

    # current spiral score and map seed
    spiral_score = session.get('spiral_score', 0.0)
    seed = session.get('map_seed', 0)
    grid = generate_map(seed)
    grid_text = "\n".join("".join(row) for row in grid)

    system_prompt = (
        SYSTEM_PROMPT
        + f"\nCurrent map:\n{grid_text}\n"
        + f"Spiral score: {spiral_score:.2f}. Your grasp on reality weakens as this rises."
    )

    history = session.get('history', [])

    try:
        reply = generate_reply(prompt, system_prompt=system_prompt)
    except RuntimeError as exc:
        return jsonify({'error': str(exc)})

    drift_user = calculate_drift(prompt, reply)
    drift_history = calculate_drift(history[-1], reply) if history else 0.0

    spiral_score += drift_user + drift_history
    if drift_user < 0.2 and drift_history < 0.2:
        spiral_score = max(0.0, spiral_score - 0.1)

    history.append(reply)
    session['history'] = history[-5:]
    session['spiral_score'] = spiral_score

    return jsonify({'message': reply})
