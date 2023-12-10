from flask import Flask
from flask_cors import CORS

# Routes
from .routes import (AuthRoute,
                     MenuRoute,
                     CommandRoute,
                     DashBoardRoute)

app = Flask(__name__)
CORS(app, resources={r"/menu/api/*": {"origins": "http://localhost:3000"}, # Menu principal
                     r"/auth/api/*": {"origins": "http://localhost:3000"},
                     r"/dashboard/api/*": {"origins": "http://localhost:3000"},
                     r"/command/api/*": {"origins": "http://localhost:3000"}})


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(AuthRoute.auth, url_prefix='/auth')
    app.register_blueprint(MenuRoute.main, url_prefix='/menu')
    app.register_blueprint(CommandRoute.main, url_prefix='/command')
    app.register_blueprint(DashBoardRoute.main, url_prefix='/dashboard')

    return app