from flask import Blueprint, jsonify, request
import json
import traceback

# Services
from src.services.DashBoardService import DashBoardServices
# Logger
from src.utils.Logger import Logger

main = Blueprint('dashboard', __name__)


@main.route('/api/projects', methods=['GET'])
def get_categories_menu():
    try:
        authorization_header = request.headers.get('Authorization')

        response, status_code = DashBoardServices.get_projects_user(authorization_header)

        return jsonify(response), status_code

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error intern", 'success': False}), 500

