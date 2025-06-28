import random
from flask import Blueprint, jsonify, request, session

from ...utils.spiral_state import analyze_map

from ...utils.map import generate_map

map_bp = Blueprint('map', __name__)


@map_bp.route('/map', methods=['GET'])
def get_map():
    """Return a procedurally generated map as JSON."""
    seed_param = request.args.get('seed')
    if seed_param is None:
        seed = random.randint(0, 2**32 - 1)
    else:
        try:
            seed = int(seed_param)
        except ValueError:
            seed = random.randint(0, 2**32 - 1)

    session['map_seed'] = seed
    grid = generate_map(seed)
    analysis = analyze_map(grid)
    location = (5, 5)
    if 0 <= location[0] < len(grid) and 0 <= location[1] < len(grid[0]):
        grid[location[0]][location[1]] = '@'
    session['map_analysis'] = analysis
    session['player_loc'] = location
    return jsonify({'seed': seed, 'grid': grid, 'analysis': analysis, 'location': location})
