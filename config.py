from decouple import config
import secrets


class Config:
    # Generar una clave secreta de 32 bytes (256 bits)
    JWT_ACCESS_SECRET = config('JWT_ACCESS_SECRET', default=secrets.token_hex(32))
    JWT_REFRESH_SECRET = config('JWT_REFRESH_SECRET', default=secrets.token_hex(32))


class DevelopmentConfig(Config):
    DEBUG = True
    FRONTEND_URL = config('DEVELOPMENT_FRONTEND_URL', default='http://localhost:3000')


class ProductionConfig(Config):
    DEBUG = False
    FRONTEND_URL = config('PRODUCTION_FRONTEND_URL', default='https://memorixanalitic.web.app')
    JWT_ACCESS_SECRET = config('JWT_ACCESS_SECRET')
    JWT_REFRESH_SECRET = config('JWT_REFRESH_SECRET')


configurations = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
