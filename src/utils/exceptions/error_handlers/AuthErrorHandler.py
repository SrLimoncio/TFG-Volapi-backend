from functools import wraps
from src.utils.Logger import Logger
#from src.utils.exceptions.AuthExceptions import
import traceback


class AuthErrorHandler:
    @staticmethod
    def auth_error_handler(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            #try:
            return f(*args, **kwargs)

            """except InvalidTokenError as ex:
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())
                return {'message': str(ex), 'isValid': False, 'isExpired': False}, 401

            except TokenExpiredError as ex:
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())
                return {'message': str(ex), 'isValid': True, 'isExpired': True}, 401"""

        return decorated_function