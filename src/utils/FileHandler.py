import traceback
import os

# Logger
from src.utils.Logger import Logger


class FileHandler:
    @classmethod
    def check_filepath(cls, filepath):
        try:
            is_correct = os.path.exists(filepath)

            return is_correct

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None