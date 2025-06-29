from flask import Blueprint, jsonify, request

from ...utils.map import generate_map, with_player_marker
from ...utils.spiral_state import analyze_map, get_available_directions
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

    dx, dy = DIRECTIONS[direction]

    state = load_game_state()
    grid = state.map_grid
    if grid is None:
        grid = generate_map(state.map_seed)
        state.map_grid = grid

    x, y = state.player_loc
    new_x = x + dx
    new_y = y + dy
    if not (0 <= new_x < len(grid) and 0 <= new_y < len(grid[0])):
        save_game_state(state)
        return jsonify({"error": "Blocked"})
    if grid[new_x][new_y] == "#":
        save_game_state(state)
        return jsonify({"error": "Blocked"})

    state.player_loc = (new_x, new_y)
    analysis = analyze_map(grid)
    location = state.player_loc
    directions = get_available_directions(grid, location)
    display = with_player_marker(grid, location)

    save_game_state(state)
    return jsonify({
        "seed": state.map_seed,
        "grid": display,
        "analysis": analysis,
        "location": location,
        "directions": directions,
    })
