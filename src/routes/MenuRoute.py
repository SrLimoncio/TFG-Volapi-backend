from flask import Blueprint, jsonify, request
import traceback

# Services
from src.services.MenuCatService import MenuCatService
# Exceptions
from src.exceptions.error_handlers.SecurityErrorHandler import SecurityErrorHandler
# Logger
from src.utils.Logger import Logger

main = Blueprint('menu', __name__)


@main.route('/api/categories', methods=['GET'])
@SecurityErrorHandler.security_error_handler
def get_categories_menu():
    """
    Ruta para obtener las categorías del menú.
    Utiliza el servicio MenuCatService para obtener las categorías.

    Excepciones:
    - Captura y registra cualquier excepción que ocurra durante la ejecución.
    """
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = MenuCatService.get_menu_cats(authorization_header)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500


@main.route('/api/info-subcat-user', methods=['GET'])
@SecurityErrorHandler.security_error_handler
def get_subcategories_user():
    """
    Ruta para obtener información de subcategorías asociadas a un usuario.
    Recoge el token de autorización y el ID de comando para solicitar al servicio.

    Excepciones:
    - Captura y registra cualquier excepción que ocurra durante la ejecución.
    """
    try:
        # Obtenemos el token del encabezado de la solicitud
        authorization_header = request.headers.get('Authorization')
        command_id = request.json.get('command_id')

        response, status_code = MenuCatService.get_info_subcat_user(authorization_header, command_id)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500
