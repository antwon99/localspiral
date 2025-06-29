import random
from flask import Blueprint, jsonify, request

from ...utils.spiral_state import analyze_map

from ...utils.map import generate_map, with_entities
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
    enemy_positions = [e.position for e in state.enemies]
    display = with_entities(state.map_grid, location, enemy_positions)
    save_game_state(state)
    char_name = None
    if isinstance(state.character, dict):
        char_name = state.character.get("display_name")
    return jsonify({
        "seed": seed,
        "grid": display,
        "analysis": analysis,
        "location": location,
        "display_name": char_name,
    })
