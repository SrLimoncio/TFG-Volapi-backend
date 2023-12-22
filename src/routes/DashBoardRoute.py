from flask import Blueprint, jsonify, request
import json
import traceback

# Services
from src.services.DashBoardService import DashBoardServices
# Logger
from src.utils.Logger import Logger

main = Blueprint('dashboard', __name__)


@main.route('/api/projects', methods=['GET'])
def get_projects_user():
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = DashBoardServices.get_projects_user(authorization_header)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500


@main.route('/api/update-name-project/<int:id_project>', methods=['PUT'])
def update_name_project(id_project):
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
def create_project():
    try:
        authorization_header = request.headers.get('Authorization')
        name = request.json.get('name')
        tool = request.json.get('tool')
        os = request.json.get('os')
        memory_path = request.json.get('memory_path')

        response, status_code = DashBoardServices.create_project(authorization_header,
                                                                 name,
                                                                 tool,
                                                                 os,
                                                                 memory_path)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500


@main.route('/api/activate-project/<int:id_project>', methods=['PUT'])
def update_active_project(id_project):
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = DashBoardServices.update_active_project(authorization_header, id_project)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False}), 500


@main.route('/api/delete-project', methods=['GET'])
def delete_project():
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = DashBoardServices.save_edit_project(authorization_header, new_name_project)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500


