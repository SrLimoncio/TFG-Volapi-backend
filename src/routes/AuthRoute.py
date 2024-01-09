from flask import Blueprint, request, jsonify

import traceback

# Logger
from src.utils.Logger import Logger
# Services
from src.services.AuthService import AuthServices

auth = Blueprint('auth', __name__)


@auth.route('/api/login', methods=['POST'])
def auth_login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        response, status_code = AuthServices.authenticate_user(email, password)

        Logger.add_to_log("info", response)
        Logger.add_to_log("info", status_code)
        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': str(ex), 'success': False}), 500


@auth.route('/api/logout', methods=['POST'])
def auth_logout():
    try:
        return ""

    except Exception as ex:
        Logger.add_to_log("api_request.log", "error", str(ex))
        Logger.add_to_log("api_request.log", "error", traceback.format_exc())
        return jsonify({'message': str(ex), 'success': False}), 500


@auth.route('/api/register', methods=['POST'])
def auth_sign_up():
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
        return jsonify({'message': str(ex), 'success': False}), 500


@auth.route('/api/check-access-token', methods=['GET'])
def auth_check_access_token():
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = AuthServices.check_access_token(authorization_header)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': str(ex), 'success': False}), 500


@auth.route('/api/renew-access-token', methods=['POST'])
def auth_check_refresh_token():
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