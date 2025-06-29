import os

import openai
from flask import Blueprint, request, jsonify

from ...utils.game_state import GAME_STATE
from ...utils.spiral import update_spiral

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")
    GAME_STATE.turn += 1
    messages = [
        {"role": "system", "content": GAME_STATE.character.get("intro_prompt", "")},
        {"role": "assistant", "content": GAME_STATE.last_narration},
        {"role": "user", "content": prompt},
    ]
    try:
        result = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages)
        response = result.choices[0].message["content"].strip()
    except Exception as exc:
        response = f"OpenAI error: {exc}"
    GAME_STATE.last_narration = response
    update_spiral(vars(GAME_STATE), prompt, response)
    return jsonify({"turn": GAME_STATE.turn, "response": response})
