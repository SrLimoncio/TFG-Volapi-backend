import traceback
import os
import hashlib

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

    @classmethod
    def calculate_hashes(cls, filepath):
        # Lee el archivo en modo binario
        with open(filepath, 'rb') as f:
            contenido = f.read()

        # Calcula SHA256
        sha256 = hashlib.sha256(contenido).hexdigest()

        # Calcula SHA1
        sha1 = hashlib.sha1(contenido).hexdigest()

        # Calcula MD5
        md5 = hashlib.md5(contenido).hexdigest()

        return sha256, sha1, md5
