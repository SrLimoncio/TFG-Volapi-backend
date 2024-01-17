from functools import wraps
from flask import jsonify
import traceback

from src.utils.Logger import Logger
from src.exceptions.AuthExceptions import InvalidCredentialsException, UserNotFoundException


class AuthErrorHandler:
    @staticmethod
    def auth_error_handler(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)

            except (InvalidCredentialsException, UserNotFoundException) as ex:
                Logger.add_to_log("error", str(ex))
                # Logger.add_to_log("error", traceback.format_exc())
                return jsonify({'message': "Unauthorized", 'success': False}), 401

        return decorated_function
