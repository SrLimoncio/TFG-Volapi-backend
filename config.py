from decouple import config
import secrets


class Config():
    # Generar una clave secreta de 32 bytes (256 bits)
    SECRET_KEY = config('SECRET_KEY', default=secrets.token_hex(32))


class DevelopmentConfig(Config):
    DEBUG = True
    JSON_AS_ASCII = False


config = {
    'development': DevelopmentConfig
}
