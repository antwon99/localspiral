from flask import Blueprint, jsonify

spiral_bp = Blueprint('spiral', __name__)

@spiral_bp.route('/spiral', methods=['GET'])
def spiral_example():
    """Placeholder spiral endpoint."""
    return jsonify({'message': 'Spiral endpoint reached.'})
