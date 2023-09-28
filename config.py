from decouple import config as decouple_config

class Config():
    SECRET_KEY = decouple_config('SECRET_KEY', default='my_default_secret_key')

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}