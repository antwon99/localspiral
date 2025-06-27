"""Entry point for the AI Spiral Simulator server."""
from flask import Flask, render_template
from .routes.chat import chat_bp
from .routes.spiral import spiral_bp
from .routes.map import map_bp


def create_app() -> Flask:
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(chat_bp)
    app.register_blueprint(spiral_bp)
    app.register_blueprint(map_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
