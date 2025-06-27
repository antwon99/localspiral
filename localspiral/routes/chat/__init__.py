from flask import Blueprint, jsonify

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['GET'])
def chat_example():
    """Placeholder chat endpoint."""
    return jsonify({'message': 'Chat endpoint reached.'})
