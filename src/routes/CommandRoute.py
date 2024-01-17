from flask import Blueprint, jsonify, request
import urllib.parse
import traceback

from src.exceptions.error_handlers.SecurityErrorHandler import SecurityErrorHandler
# Services
from src.services.CommandService import CommandService
# Logger
from src.utils.Logger import Logger

main = Blueprint('command', __name__)


@main.route('/api/exe-vol-command', methods=['GET'])
@SecurityErrorHandler.security_error_handler
def execute_volatility_command():
    """
    Ruta para ejecutar un comando de Volatility.
    Espera un 'command_id' y opciones adicionales a través de la cadena de consulta (query string).
    """
    try:
        authorization_header = request.headers.get('Authorization')
        command_id = request.args.get('command_id')
        if command_id is None:
            return jsonify({'message': 'Command ID is required', 'success': False}), 400

        options_query = request.args.get('options', '')

        # Deserializar las opciones
        options_pairs = urllib.parse.parse_qsl(options_query)
        options = {int(k): v for k, v in options_pairs}

        Logger.add_to_log("info", f"Options: {options}")

        response, status_code = CommandService.execute_volatility_command(authorization_header, command_id, options)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500


@main.route('/api/show-vol-command', methods=['GET'])
@SecurityErrorHandler.security_error_handler
def show_volatility_command():
    """
    Ruta para mostrar los resultados de un comando de Volatility.
    Requiere un 'command_id' a través de la cadena de consulta.
    """
    try:
        authorization_header = request.headers.get('Authorization')
        command_id = request.args.get('command_id')
        if command_id is None:
            return jsonify({'message': 'Command ID is required', 'success': False}), 400

        response, status_code = CommandService.show_volatility_command(authorization_header, command_id)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500


@main.route('/api/delete-result-cmd/<int:command_id>', methods=['DELETE'])
@SecurityErrorHandler.security_error_handler
def delete_result_command(command_id):
    """
    Ruta para eliminar el resultado de un comando de Volatility.
    Requiere un 'command_id' como parte de la URL.
    """
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = CommandService.delete_result_command(authorization_header, command_id)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500
