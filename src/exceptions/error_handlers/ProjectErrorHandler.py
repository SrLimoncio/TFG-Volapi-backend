from functools import wraps
from src.utils.Logger import Logger
from src.exceptions.ProjectExceptions import DuplicateProjectCustom, NotValidInputsProjectCustom
import traceback


class ProjectErrorHandler:
    @staticmethod
    def project_error_handler(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)

            except DuplicateProjectCustom as ex:
                Logger.add_to_log("error", str(ex))
                # Logger.add_to_log("error", traceback.format_exc())
                return {'message': str(ex), 'isValid': False, 'projectExist': True}, 409

            except NotValidInputsProjectCustom as ex:
                Logger.add_to_log("error", str(ex))
                # Logger.add_to_log("error", traceback.format_exc())
                return {'message': str(ex), 'isValid': False, 'projectExist': False}, 409

        return decorated_function
