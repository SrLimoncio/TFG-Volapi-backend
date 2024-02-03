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

    frontend_url = app.config['FRONTEND_URL']
    CORS(app, resources={
        r"/auth/api/*": {"origins": frontend_url},
        r"/menu/api/*": {"origins": frontend_url},
        r"/command/api/*": {"origins": frontend_url},
        r"/dashboard/api/*": {"origins": frontend_url}
        },
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"]
    )

    # Blueprints
    app.register_blueprint(AuthRoute.auth, url_prefix='/auth')
    app.register_blueprint(MenuRoute.main, url_prefix='/menu')
    app.register_blueprint(CommandRoute.main, url_prefix='/command')
    app.register_blueprint(DashBoardRoute.main, url_prefix='/dashboard')

    return app
