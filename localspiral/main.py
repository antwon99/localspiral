from flask import Flask, render_template

from .utils import game_state

from .routes.chat import chat_bp
from .routes.spiral import spiral_bp
from .routes.game import game_bp

app = Flask(__name__, template_folder="templates")

# Register blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(spiral_bp)
app.register_blueprint(game_bp)


@app.route("/")
def index():
    return render_template(
        "index.html",
        narration=game_state.GAME_STATE.last_narration,
        spiral=game_state.GAME_STATE.spiral,
    )


if __name__ == "__main__":
    app.run(debug=True)
