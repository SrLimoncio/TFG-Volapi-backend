import traceback

# Security
from src.utils.Security import Security
# Models
from src.models.AuthModel import AuthModel
from src.models.UserModel import UserModel
from src.utils.Logger import Logger

# Excepciones
from src.utils.exceptions.error_handlers.SecurityErrorHandler import SecurityErrorHandler


class AuthServices:
    @classmethod
    @SecurityErrorHandler.security_error_handler
    def authenticate_user(cls, email, provided_password):
        user = AuthModel.validate_login(email, provided_password)
        Logger.add_to_log("info", user)

        if user:
            # Si la autenticación es exitosa, generamos un token y lo devolvemos
            access_token = Security.generate_access_token(user.id)
            refresh_token = Security.generate_refresh_token(user.id)

            return {'message': "Successful login", 'access_token': access_token,
                    'refresh_token': refresh_token, 'success': True}, 200

        else:
            # Si la autenticación falla, devolvemos un mensaje de error
            return {'message': "The credentials entered are incorrect. Please verify your email and password.",
                    'success': False}, 401

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def register_user(cls, email, password, password2, username, name):
        # Verifica los campos
        error_fields = AuthModel.validate_registration(email, password, password2, username, name)
        if error_fields:
            return {'message': "Error en la solicitud", 'error_fields': error_fields, 'success': False}, 400

        # Hash de la contraseña antes de almacenarla en la base de datos
        hashed_password = AuthModel.generate_password_hash(password)

        # Crea un nuevo usuario en la base de datos
        UserModel.create_user(email, hashed_password, username, name)

        user = UserModel(0, email, password, username, name)
        # Genera un token JWT para el nuevo usuario
        token = Security.generate_access_token(user.id)

        return {'message': "Registro exitoso", 'success': True, 'token': token}, 201

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def check_access_token(cls, encoded_access_token):
        user_id = Security.verify_access_token(encoded_access_token)
        if user_id:
            return {'message': "Successful", 'isValid': True, 'success': True}, 201
        else:
            return {'message': "Successful", 'isValid': False, 'success': False}, 401

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def renew_access_token(cls, encoded_failed_access_token, encoded_refresh_token):
        # Verificamos el token de refresco que sea valido y no este caducado
        refresh_token_user_id = Security.verify_refresh_token(encoded_refresh_token)
        expired_access_token_user_id = Security.verify_expired_access_token(encoded_refresh_token)
        Logger.add_to_log("info", refresh_token_user_id)
        Logger.add_to_log("info", expired_access_token_user_id)

        if refresh_token_user_id == expired_access_token_user_id:
            new_access_token = Security.generate_access_token(refresh_token_user_id)
            return {'message': "Successful", 'newAccessToken': new_access_token, 'success': True}, 201
        else:
            return {'message': "Error authentication", 'success': False}, 201
