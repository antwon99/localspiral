from flask import Blueprint, jsonify, request

from ...utils.map import generate_map, with_entities
from ...utils.zones import ensure_zone_map, at_door, move_to_next_zone
from ...utils.spiral_state import analyze_map, get_available_directions
from ...utils.game_loop import apply_move, advance_state, handle_enemy_encounters
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
        zones = getattr(state, "zones", [])
        if zones:
            grid = ensure_zone_map(state.map_seed, zones[state.zone_index], state.zone_index)
        else:
            grid = generate_map(state.map_seed)
        state.map_grid = grid

    if not apply_move(state, direction):
        save_game_state(state)
        return jsonify({"error": "Blocked"}), 400

    state.turn_count += 1
    zone_msg = None
    if at_door(state.map_grid, state.player_loc):
        zone_msg = move_to_next_zone(state)
        grid = state.map_grid

    advance_state(state)
    handle_enemy_encounters(state)

    state.spiral_score = max(0.0, state.spiral_score - 0.07)
    state.paranoia_level = max(0.0, min(10.0, state.paranoia_level + 0.05))
    state.update_sanity()

    analysis = analyze_map(grid)
    location = state.player_loc
    directions = get_available_directions(grid, location)
    enemy_positions = [e.position for e in state.enemies]
    display = with_entities(grid, location, enemy_positions)

    save_game_state(state)
    zone_name = None
    if getattr(state, "zones", None):
        zone_name = state.zones[state.zone_index].name
    return jsonify({
        "seed": state.map_seed,
        "grid": display,
        "analysis": analysis,
        "location": location,
        "directions": directions,
        "zone": zone_name,
        "message": zone_msg,
    })
