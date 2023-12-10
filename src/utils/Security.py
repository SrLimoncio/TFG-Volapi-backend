from decouple import config

import datetime
import jwt
import pytz
import traceback

# Logger
from src.utils.Logger import Logger


class Security:
    secret = config('JWT_KEY')
    tz = pytz.timezone("Europe/Madrid")

    @classmethod
    def generate_token(cls, authenticated_user):
        try:
            payload = {
                'iat': datetime.datetime.now(tz=cls.tz),
                'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=60),
                'id': authenticated_user.id
            }
            return jwt.encode(payload, cls.secret, algorithm="HS256")
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def verify_token(cls, encoded_token):
        try:
            # Verifica si el encabezado de Autorización está presente y tiene el formato correcto
            if encoded_token and encoded_token.startswith('Bearer '):
                jwt_token = encoded_token.split(' ')[1]
                try:
                    payload = jwt.decode(jwt_token, cls.secret, algorithms=["HS256"])

                    # Verificar la expiración del token
                    expiration_time = datetime.datetime.fromtimestamp(payload['exp'], tz=cls.tz)
                    current_time = datetime.datetime.now(tz=cls.tz)

                    if current_time > expiration_time:
                        # Token ha expirado
                        return None

                    return payload
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return None
            return None

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None
