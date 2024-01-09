from config import configurations
from src import init_app
import os

environment = os.environ.get('FLASK_ENV', 'development')
app_config = configurations[environment]
app = init_app(app_config)


if __name__ == '__main__':
    app.run()