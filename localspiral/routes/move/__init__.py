from flask import Blueprint, jsonify, request

from ...utils.map import generate_map, with_entities
from ...utils.spiral_state import analyze_map, get_available_directions
from ...utils.game_loop import apply_move, advance_state
from ...utils.state import load_game_state, save_game_state

move_bp = Blueprint("move", __name__)

DIRECTIONS = {
    "north": (-1, 0),
    "south": (1, 0),
    "west": (0, -1),
    "east": (0, 1),
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}


@move_bp.route("/move", methods=["GET"])
def move_player():
    """Move the player if the destination is valid."""
    direction = request.args.get("dir", "").lower()
    if direction not in DIRECTIONS:
        return jsonify({"error": "Invalid direction"}), 400

    state = load_game_state()
    grid = state.map_grid
    if grid is None:
        grid = generate_map(state.map_seed)
        state.map_grid = grid

    if not apply_move(state, direction):
        save_game_state(state)
        return jsonify({"error": "Blocked"}), 400

    state.turn_count += 1
    advance_state(state)
    analysis = analyze_map(grid)
    location = state.player_loc
    directions = get_available_directions(grid, location)
    enemy_positions = [e.position for e in state.enemies]
    display = with_entities(grid, location, enemy_positions)

    save_game_state(state)
    return jsonify({
        "seed": state.map_seed,
        "grid": display,
        "analysis": analysis,
        "location": location,
        "directions": directions,
    })
