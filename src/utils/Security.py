from decouple import config
import datetime
import jwt
import pytz
import traceback
import bcrypt

# Exceptions
from src.exceptions.SecurityExceptions import (GeneralTokenError, GeneratingTokenError,
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
    def generate_password_hash(cls, password):
        """
        Genera un hash seguro para una contraseña.

        Args:
            password (str): La contraseña a hashear.

        Returns:
            str: La contraseña hasheada.
        """

        # Método para generar un hash seguro de una contraseña antes de almacenarla en la base de datos.
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    @classmethod
    def verify_password(cls, provided_password, hashed_password):
        """
        Verifica si una contraseña proporcionada coincide con su hash.

        Args:
            provided_password (str): Contraseña proporcionada.
            hashed_password (str): Hash de la contraseña almacenada.

        Returns:
            bool: True si las contraseñas coinciden, False en caso contrario.
        """

        # Método para verificar si la contraseña proporcionada coincide
        # con la contraseña almacenada en la base de datos.
        if isinstance(provided_password, str):
            provided_password = provided_password.encode('utf-8')
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')

        return bcrypt.checkpw(provided_password, hashed_password)

    @classmethod
    def generate_access_token(cls, user_id):
        """
        Genera un token de acceso JWT para un usuario.

        Args:
            user_id (int): ID del usuario para el cual se genera el token.

        Returns:
            str: El token de acceso JWT.

        Raises:
            GeneratingTokenError: Si ocurre un error al generar el token.
        """

        try:
            current_time = datetime.datetime.now(tz=cls.tz)
            payload = {
                'iat': current_time,
                'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(hours=1),
                # 'exp': current_time + datetime.timedelta(minutes=10),
                'id': user_id
            }
            return jwt.encode(payload, cls.access_secret, algorithm="HS256")

        except jwt.PyJWTError as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise GeneratingTokenError() from ex

    @classmethod
    def generate_refresh_token(cls, user_id):
        """
        Genera un token de refresco JWT para un usuario.

        Args:
            user_id (int): ID del usuario para el cual se genera el token.

        Returns:
            str: El token de refresco JWT.

        Raises:
            GeneratingTokenError: Si ocurre un error al generar el token.
        """

        try:
            current_time = datetime.datetime.now(tz=cls.tz)
            payload = {
                'iat': current_time,
                'exp': current_time + datetime.timedelta(days=3),
                # 'exp': current_time + datetime.timedelta(minutes=20),
                'id': user_id
            }
            return jwt.encode(payload, cls.refresh_secret, algorithm="HS256")

        except jwt.PyJWTError as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise GeneratingTokenError() from ex

    @classmethod
    def verify_token(cls, encoded_token, type_token):
        """
        Verifica la validez de un token JWT.

        Args:
            encoded_token (str): Token codificado.
            type_token (str): Tipo de token (ACCESS o REFRESH).

        Returns:
            int: El ID del usuario del token.

        Raises:
            InvalidTokenError: Si el token no es válido.
            TokenExpiredError: Si el token ha expirado.
        """

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
        """
        Verifica la validez de un token de acceso.

        Args:
            encoded_token (str): Token de acceso codificado.

        Returns:
            int: ID del usuario si el token es válido.

        Raises:
            InvalidTokenError: Si el token no es válido o si falta.
            TokenExpiredError: Si el token ha expirado.
        """

        return cls.verify_token(encoded_token, cls.TYPE_ACCESS_TOKEN)

    @classmethod
    def verify_refresh_token(cls, encoded_token):
        """
        Verifica la validez de un token de refresco.

        Args:
            encoded_token (str): Token de refresco codificado.

        Returns:
            int: ID del usuario si el token es válido.

        Raises:
            InvalidTokenError: Si el token no es válido o si falta.
            TokenExpiredError: Si el token ha expirado.
        """

        return cls.verify_token(encoded_token, cls.TYPE_REFRESH_TOKEN)

    @classmethod
    def verify_expired_access_token(cls, encoded_token):
        """
        Verifica un token de acceso expirado, utilizada para renovar token.

        Args:
            encoded_token (str): Token de acceso expirado codificado.

        Returns:
            int: ID del usuario si el token es válido.

        Raises:
            InvalidTokenError: Si el token no es válido o si falta.
        """

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
