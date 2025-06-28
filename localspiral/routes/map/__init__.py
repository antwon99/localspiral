import random
from flask import Blueprint, jsonify, request

from ...utils.spiral_state import analyze_map

from ...utils.map import generate_map
from ...utils.state import load_game_state, save_game_state

map_bp = Blueprint("map", __name__)


@map_bp.route("/map", methods=["GET"])
def get_map():
    """Return a procedurally generated map as JSON."""
    seed_param = request.args.get("seed")
    if seed_param is None:
        seed = random.randint(0, 2**32 - 1)
    else:
        try:
            seed = int(seed_param)
        except ValueError:
            seed = random.randint(0, 2**32 - 1)

    state = load_game_state()
    state.map_seed = seed
    grid = generate_map(seed)
    state.map_grid = grid
    analysis = analyze_map(grid)
    location = state.player_loc
    if 0 <= location[0] < len(grid) and 0 <= location[1] < len(grid[0]):
        grid[location[0]][location[1]] = "@"
    save_game_state(state)
    return jsonify({"seed": seed, "grid": grid, "analysis": analysis, "location": location})
