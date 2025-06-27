from flask import Blueprint, jsonify, request

from ...utils.map import generate_map

map_bp = Blueprint('map', __name__)


@map_bp.route('/map', methods=['GET'])
def get_map():
    """Return a procedurally generated map as JSON."""
    seed_str = request.args.get('seed', '0')
    try:
        seed = int(seed_str)
    except ValueError:
        seed = 0
    grid = generate_map(seed)
    return jsonify({'grid': grid})
