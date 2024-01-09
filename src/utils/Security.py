from decouple import config

import datetime
import jwt
import pytz
import traceback

# Exceptions
from src.utils.exceptions.SecurityExceptions import (GeneralTokenError, GeneratingTokenError,
                                                     InvalidTokenError, TokenExpiredError)
# Logger
from src.utils.Logger import Logger


class Security:
    TYPE_ACCESS_TOKEN = 'ACCESS'
    TYPE_REFRESH_TOKEN = 'REFRESH'
    access_secret = config('JWT_ACCESS_SECRET')
    refresh_secret = config('JWT_REFRESH_SECRET')
    tz = pytz.timezone("Europe/Madrid")

    @classmethod
    def generate_access_token(cls, user_id):
        try:
            current_time = datetime.datetime.now(tz=cls.tz)
            payload = {
                'iat': current_time,
                # 'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(hours=1),
                'exp': current_time + datetime.timedelta(minutes=10),
                'id': user_id
            }
            return jwt.encode(payload, cls.access_secret, algorithm="HS256")

        except jwt.PyJWTError as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise GeneratingTokenError() from ex

    @classmethod
    def generate_refresh_token(cls, user_id):
        try:
            current_time = datetime.datetime.now(tz=cls.tz)
            payload = {
                'iat': current_time,
                #'exp': current_time + datetime.timedelta(days=3),
                'exp': current_time + datetime.timedelta(minutes=20),
                'id': user_id
            }
            return jwt.encode(payload, cls.refresh_secret, algorithm="HS256")

        except jwt.PyJWTError as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise GeneratingTokenError() from ex

    @classmethod
    def verify_token(cls, encoded_token, type_token):
        try:
            # Verifica si el encabezado de Autorización está presente y tiene el formato correcto
            if not (encoded_token and encoded_token.lower().startswith('bearer')):
                raise InvalidTokenError()

            parts = encoded_token.split(' ')
            if not (len(parts) >= 2 and parts[1]):
                raise InvalidTokenError()

            if type_token not in [cls.TYPE_ACCESS_TOKEN, cls.TYPE_REFRESH_TOKEN]:
                raise GeneralTokenError("Invalid token type specified")

            secret = None
            if type_token == cls.TYPE_ACCESS_TOKEN:
                secret = cls.access_secret
            if type_token == cls.TYPE_REFRESH_TOKEN:
                secret = cls.refresh_secret

            jwt_token = parts[1]
            payload = jwt.decode(jwt_token, secret, algorithms=["HS256"])

            if (not ('id' in payload or payload['id'])) or (not ('exp' in payload or payload['exp'])):
                raise InvalidTokenError()

            # Verificar la expiración del token
            expiration_time = datetime.datetime.fromtimestamp(payload['exp'], tz=cls.tz)
            current_time = datetime.datetime.now(tz=cls.tz)

            if current_time >= expiration_time:
                # Token ha expirado
                raise TokenExpiredError()

            return payload['id']

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()

        except jwt.InvalidSignatureError:
            raise InvalidTokenError()

        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    @classmethod
    def verify_access_token(cls, encoded_token):
        return cls.verify_token(encoded_token, cls.TYPE_ACCESS_TOKEN)

    @classmethod
    def verify_refresh_token(cls, encoded_token):
        return cls.verify_token(encoded_token, cls.TYPE_REFRESH_TOKEN)

    @classmethod
    def verify_expired_access_token(cls, encoded_token):
        try:
            # Verifica si el encabezado de Autorización está presente y tiene el formato correcto
            if not (encoded_token and encoded_token.lower().startswith('bearer')):
                raise InvalidTokenError()

            parts = encoded_token.split(' ')
            if not (len(parts) >= 2 and parts[1]):
                raise InvalidTokenError()

            jwt_token = parts[1]
            payload = jwt.decode(jwt_token, cls.access_secret, algorithms=["HS256"], options={"verify_exp": False})

            if (not ('id' in payload or payload['id'])) or (not ('exp' in payload or payload['exp'])):
                raise InvalidTokenError()

            return payload['id']

        except jwt.InvalidSignatureError:
            raise InvalidTokenError()

        except jwt.InvalidTokenError:
            raise InvalidTokenError()
