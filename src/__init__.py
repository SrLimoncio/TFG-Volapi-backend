from flask import Flask
from flask_cors import CORS

# Routes
from .routes import (AuthRoute,
                     MenuRoute,
                     CommandRoute,
                     DashBoardRoute)


def init_app(config):
    app = Flask(__name__)
    # Configuration
    app.config.from_object(config)

    CORS(app, resources={r"/menu/api/*": {"origins": app.config['FRONTEND_URL']},  # Menu principal
                         r"/auth/api/*": {"origins": app.config['FRONTEND_URL']},
                         r"/dashboard/api/*": {"origins": app.config['FRONTEND_URL']},
                         r"/command/api/*": {"origins": app.config['FRONTEND_URL']}
                         })

    # Blueprints
    app.register_blueprint(AuthRoute.auth, url_prefix='/auth')
    app.register_blueprint(MenuRoute.main, url_prefix='/menu')
    app.register_blueprint(CommandRoute.main, url_prefix='/command')
    app.register_blueprint(DashBoardRoute.main, url_prefix='/dashboard')

    return app
