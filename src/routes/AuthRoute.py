from flask import Blueprint, request, jsonify
import traceback

# Services
from src.services.AuthService import AuthServices
# Exceptions
from src.exceptions.error_handlers.SecurityErrorHandler import SecurityErrorHandler
from src.exceptions.error_handlers.AuthErrorHandler import AuthErrorHandler
# Logger
from src.utils.Logger import Logger

auth = Blueprint('auth', __name__)


@auth.route('/api/register', methods=['POST'])
@SecurityErrorHandler.security_error_handler
@AuthErrorHandler.auth_error_handler
def auth_register():
    """
    Procesa el registro de nuevos usuarios. Recoge los datos de registro desde el cuerpo de la solicitud.
    """
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        password2 = request.json.get('password2')
        username = request.json.get('username')
        name = request.json.get('name')

        response, status_code = AuthServices.register_user(email, password, password2, username, name)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal error", 'success': False}), 500


@auth.route('/api/login', methods=['POST'])
@SecurityErrorHandler.security_error_handler
@AuthErrorHandler.auth_error_handler
def auth_login():
    """
    Autentica a un usuario. Recoge las credenciales de inicio de sesión desde el cuerpo de la solicitud.
    """
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        response, status_code = AuthServices.authenticate_user(email, password)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': str(ex), 'success': False}), 500


@SecurityErrorHandler.security_error_handler
@auth.route('/api/check-access-token', methods=['GET'])
def auth_check_access_token():
    """
    Verifica la validez del token de acceso proporcionado en el encabezado de la solicitud.
    """
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = AuthServices.check_access_token(authorization_header)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': str(ex), 'success': False}), 500


@SecurityErrorHandler.security_error_handler
@auth.route('/api/renew-access-token', methods=['POST'])
def auth_renew_access_token():
    """
    Renueva el token de acceso utilizando un token de actualización proporcionado en el encabezado de la solicitud.
    """
    try:
        failed_access_token = request.headers.get('Failed-Access-Token')
        refresh_token = request.headers.get('Refresh-Token')

        response, status_code = AuthServices.renew_access_token(failed_access_token, refresh_token)
        Logger.add_to_log("info", response)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': str(ex), 'success': False}), 500
