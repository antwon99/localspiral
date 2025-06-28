from flask import Blueprint, jsonify, request

from ...utils.spiral import get_meter, reset_meter, meter_state

spiral_bp = Blueprint('spiral', __name__)

@spiral_bp.route('/spiral', methods=['GET'])
def spiral_example():
    """Return the current spiral meter value for this session."""
    session_id = request.args.get('session', 'default')
    if request.args.get('reset') == '1':
        reset_meter(session_id)
    meter = get_meter(session_id)
    return jsonify({'score': round(meter, 3), 'sanity': meter_state(meter)})
