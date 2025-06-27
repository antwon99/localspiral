from flask import Blueprint, jsonify, request

from ...utils.dialogue import generate_reply

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

    try:
        reply = generate_reply(prompt, system_prompt=SYSTEM_PROMPT)
    except RuntimeError as exc:
        return jsonify({'error': str(exc)})

    return jsonify({'message': reply})
