from flask import Flask

# Routes
from .routes import *

app = Flask(__name__)

def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    #app.register_blueprint(Inde)

    return app