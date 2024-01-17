from src.exceptions.AuthExceptions import InvalidCredentialsException
# Security
from src.utils.Security import Security
# Models
from src.models.AuthModel import AuthModel
from src.models.UserModel import UserModel

# Exceptions
from src.exceptions.SecurityExceptions import InvalidTokenError


class AuthServices:
    @classmethod
    def register_user(cls, email, password, password2, username, name):
        """
        Registra un nuevo usuario en el sistema.

        Args:
            email (str): Email del usuario.
            password (str): Contraseña del usuario.
            password2 (str): Confirmación de la contraseña.
            username (str): Nombre de usuario.
            name (str): Nombre completo del usuario.

        Returns:
            dict, int: Respuesta con mensaje y código de estado HTTP.
        """
        # Verifica los campos
        error_fields = AuthModel.validate_registration(email, password, password2, username, name)
        if error_fields:
            return {'message': "Error en la solicitud", 'error_fields': error_fields, 'success': False}, 400

        # Hash de la contraseña antes de almacenarla en la base de datos
        hashed_password = Security.generate_password_hash(password)

        # Crea un nuevo usuario en la base de datos
        UserModel.create_user(email, hashed_password, username, name)

        return {'message': "Creacion del ususario exitosa", 'success': True}, 201

    @classmethod
    def authenticate_user(cls, email, provided_password):
        """
        Autentica a un usuario en el sistema.

        Args:
            email (str): Email del usuario.
            provided_password (str): Contraseña proporcionada por el usuario.

        Returns:
            dict, int: Respuesta con mensaje, tokens y código de estado HTTP.
        """
        user = AuthModel.authenticate_user(email, provided_password)

        if user:
            # Si la autenticación es exitosa, generamos un token y lo devolvemos
            access_token = Security.generate_access_token(user.id)
            refresh_token = Security.generate_refresh_token(user.id)

            return {'message': "Successful login", 'access_token': access_token,
                    'refresh_token': refresh_token, 'success': True}, 200
        else:
            raise InvalidCredentialsException("Error Auth: The credentials entered are incorrect.")

    @classmethod
    def check_access_token(cls, encoded_access_token):
        """
        Verifica la validez de un token de acceso.

        Args:
            encoded_access_token (str): Token de acceso codificado.

        Returns:
            dict, int: Respuesta con mensaje y código de estado HTTP.
        """
        user_id = Security.verify_access_token(encoded_access_token)
        return {'message': "Successful", 'isValid': True, 'success': True}, 200

    @classmethod
    def renew_access_token(cls, encoded_failed_access_token, encoded_refresh_token):
        """
        Renueva un token de acceso utilizando un token de refresco.

        Args:
            encoded_failed_access_token (str): Token de acceso caducado codificado.
            encoded_refresh_token (str): Token de refresco codificado.

        Returns:
            dict, int: Respuesta con mensaje, nuevo token de acceso y código de estado HTTP.
        """

        # Verificamos el token de refresco que sea valido y no este caducado
        refresh_token_user_id = Security.verify_refresh_token(encoded_refresh_token)
        expired_access_token_user_id = Security.verify_expired_access_token(encoded_refresh_token)

        if refresh_token_user_id == expired_access_token_user_id:
            new_access_token = Security.generate_access_token(refresh_token_user_id)
            return {'message': "Successful", 'newAccessToken': new_access_token, 'success': True}, 201
        else:
            raise InvalidTokenError("El token de acceso y de refresco no pertenecen al mismo usuario")
