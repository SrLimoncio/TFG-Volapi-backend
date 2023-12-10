import traceback

# Security
from src.utils.Security import Security
# Models
from src.models.AuthModel import AuthModel
from src.models.UserModel import UserModel
from src.utils.Logger import Logger

class AuthServices:
    @classmethod
    def authenticate_user(cls, email, provided_password):
        user = AuthModel.validate_login(email, provided_password)

        if user:
            # Si la autenticación es exitosa, generamos un token y lo devolvemos
            token = Security.generate_token(user)

            return {'message': "Successful login", 'token': token, 'success': True}, 200

        else:
            # Si la autenticación falla, devolvemos un mensaje de error
            return {'message': "The credentials entered are incorrect. Please verify your email and password.",
                    'success': False}, 401

    @classmethod
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
        token = Security.generate_token(user)

        return {'message': "Registro exitoso", 'success': True, 'token': token}, 201

    @classmethod
    def check_token(cls, encoded_token):
        # Verifica los campos
        if encoded_token:
            payload_token = Security.verify_token(encoded_token)
            if payload_token:
                return {'message': "OK", 'success': True}, 201
            else:
                # Devuelve un error si el token no es válido
                return {'message': 'Token de autorización no válido', 'success': False}, 401
        else:
            return {'message': 'Token de autorización no válido', 'success': False}, 401
