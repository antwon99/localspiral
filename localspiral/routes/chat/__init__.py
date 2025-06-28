from flask import Blueprint, jsonify, request

from ...utils.dialogue import generate_reply
from ...utils.scoring import calculate_drift
from ...utils.spiral import update_meter

SYSTEM_PROMPT = (
    "You are Tyler Scienceman, a helpful scientist with a stoic tone."
)

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['GET'])
def chat_example():
    """Return a dynamic response from the OpenAI API."""
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({'message': 'No prompt provided.'})

    session_id = request.args.get('session', 'default')

    try:
        reply = generate_reply(prompt, system_prompt=SYSTEM_PROMPT)
    except RuntimeError as exc:
        return jsonify({'error': str(exc)})

    drift = calculate_drift(prompt, reply)
    meter = update_meter(session_id, drift)

    return jsonify({'message': reply, 'spiral': meter})
