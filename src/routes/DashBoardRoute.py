from flask import Blueprint, jsonify, request
import traceback

from src.exceptions.FileExceptions import FileCustomException
from src.exceptions.error_handlers.ProjectErrorHandler import ProjectErrorHandler
from src.exceptions.error_handlers.SecurityErrorHandler import SecurityErrorHandler
# Services
from src.services.DashBoardService import DashBoardServices
# Logger
from src.utils.Logger import Logger

main = Blueprint('dashboard', __name__)


@main.route('/api/user-has-projects', methods=['GET'])
@SecurityErrorHandler.security_error_handler
@ProjectErrorHandler.project_error_handler
def user_has_projects():
    """
    Verifica si el usuario tiene proyectos. Utiliza el token de autenticación
    para identificar al usuario y consultar sus proyectos.
    """
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = DashBoardServices.user_has_projects(authorization_header)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False}), 500


@main.route('/api/projects', methods=['GET'])
@SecurityErrorHandler.security_error_handler
@ProjectErrorHandler.project_error_handler
def get_projects_user():
    """
    Obtiene los proyectos asociados a un usuario. Utiliza el token de autenticación
    para identificar al usuario y obtener sus proyectos.
    """
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = DashBoardServices.get_projects_user(authorization_header)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False}), 500


@main.route('/api/update-name-project/<int:id_project>', methods=['PUT'])
@SecurityErrorHandler.security_error_handler
@ProjectErrorHandler.project_error_handler
def update_name_project(id_project):
    """
    Actualiza el nombre de un proyecto específico. Requiere el ID del proyecto
    y el nuevo nombre como parte de la solicitud.
    """
    try:
        authorization_header = request.headers.get('Authorization')
        new_name_project = request.json.get('new_nameProject')

        response, status_code = DashBoardServices.update_name_project(authorization_header, id_project, new_name_project)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False}), 500


@main.route('/api/create-project', methods=['POST'])
@SecurityErrorHandler.security_error_handler
@ProjectErrorHandler.project_error_handler
def create_project():
    """
    Crea un nuevo proyecto. Recoge los detalles del proyecto desde el cuerpo
    de la solicitud y los procesa.
    """
    try:
        authorization_header = request.headers.get('Authorization')

        # Obtener datos del formulario
        name = request.json.get('name')
        tool = request.json.get('tool')
        os = request.json.get('os')

        Logger.add_to_log("error", name)
        Logger.add_to_log("error", tool)
        Logger.add_to_log("error", os)

        response, status_code = DashBoardServices.create_project(authorization_header,
                                                                 name,
                                                                 tool,
                                                                 os)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False}), 500


@main.route('/api/upload-chunk-file', methods=['POST'])
@SecurityErrorHandler.security_error_handler
@ProjectErrorHandler.project_error_handler
def upload_chunk_file():
    """
    Maneja la carga de fragmentos de archivo para un proyecto. Recoge información
    sobre el fragmento y el proyecto desde la solicitud.
    """
    global project_id
    try:
        authorization_header = request.headers.get('Authorization')

        project_id = request.form['projectId']
        chunk = request.files['chunk']
        chunk_number = request.form['chunkNumber']
        total_chunks = request.form.get('totalChunks')
        file_name = request.form.get('fileName')

        response, status_code = DashBoardServices.upload_chunk_file(authorization_header,
                                                                    project_id,
                                                                    chunk,
                                                                    chunk_number,
                                                                    total_chunks,
                                                                    file_name)

        return jsonify(response), status_code

    except FileCustomException as ex:
        DashBoardServices.delete_project(project_id)
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False}), 500

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False}), 500


@main.route('/api/activate-project/<int:id_project>', methods=['PUT'])
@SecurityErrorHandler.security_error_handler
@ProjectErrorHandler.project_error_handler
def update_active_project(id_project):
    """
    Activa un proyecto específico para un usuario. Cambia el estado del proyecto
    a activo basado en su ID.
    """
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = DashBoardServices.update_active_project(authorization_header, id_project)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False}), 500


@main.route('/api/delete-project/<int:id_project>', methods=['DELETE'])
@SecurityErrorHandler.security_error_handler
@ProjectErrorHandler.project_error_handler
def delete_project(id_project):
    """
    Elimina un proyecto específico. Requiere el ID del proyecto para
    identificar y eliminar el proyecto.
    """
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = DashBoardServices.delete_project(authorization_header, id_project)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False}), 500


