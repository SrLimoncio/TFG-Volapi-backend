from flask import Blueprint, jsonify, request
import json
import traceback

# Services
from src.services.CommandService import CommandService
# Logger
from src.utils.Logger import Logger

main = Blueprint('command', __name__)


@main.route('/api/exe-vol-command', methods=['GET'])
def execute_volatility_command():
    try:
        authorization_header = request.headers.get('Authorization')
        command_id = request.args.get('command_id')

        response, status_code = CommandService.execute_volatility_command(authorization_header, command_id)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500


@main.route('/api/show-vol-command', methods=['GET'])
def show_volatility_command():
    try:
        authorization_header = request.headers.get('Authorization')
        command_id = request.args.get('command_id')

        response, status_code = CommandService.show_volatility_command(authorization_header, command_id)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500
