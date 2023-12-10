from flask import Blueprint, request, jsonify

import traceback

# Logger
from src.utils.Logger import Logger
# Security
# src.utils.Security import Security
# Services
from src.services.HeroService import HeroServices

hero = Blueprint('hero', __name__)


@hero.route('/api/save-path', methods=['POST'])
def push_pathfile_db():
    try:
        # Variables que recibimos en el post
        token = request.json.get('token')
        filepath = request.json.get('path')
        # Comprobamos si el path del fichero es correcto
        if not filepath:
            return jsonify({'message': "Blank path", 'token': None, 'exists': False, 'success': False}), 400

        _token, is_correct = HeroServices.save_filepath(token, filepath)

        if is_correct:
            Logger.add_to_log("info", _token)
            return jsonify({'message': "Correct", 'token': _token, 'exists': True, 'success': True}), 200
        else:
            return jsonify({'message': "Path not exist", 'token': None, 'exists': False, 'success': True}), 200

    except Exception as ex:
        Logger.add_to_log("api_request.log", "error", str(ex))
        Logger.add_to_log("api_request.log", "error", traceback.format_exc())
        return jsonify({'message': str(ex), 'token': None, 'exists': False, 'success': False}), 500
