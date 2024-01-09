from flask import Blueprint, request, jsonify

import traceback

# Logger
from src.utils.Logger import Logger
# Services
# from src.services.AuthService import AuthServices

yara = Blueprint('yara', __name__)


@yara.route('/execute-rule', methods=['GET'])
def auth_login():
    try:
        return "jsonify(response), status_code"

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': str(ex), 'success': False}), 500