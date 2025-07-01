"""Entry point for the AI Spiral Simulator server."""
from flask import Flask, render_template
from .routes.chat import chat_bp
from .routes.spiral import spiral_bp
from .routes.map import map_bp
from .routes.reset import reset_bp


def create_app() -> Flask:
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'dev'
    app.register_blueprint(chat_bp)
    app.register_blueprint(spiral_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(reset_bp)

    @app.route('/')
    def landing():
        return render_template('landing.html')

    @app.route('/play')
    def index():
        return render_template('index.html')

    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
