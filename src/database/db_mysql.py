from decouple import config

import pymysql
import traceback

# Logger
from src.utils.Logger import Logger

def get_connection():
    try:
        return pymysql.connect(
            host=config('DB_HOST', default='localhost'),
            user=config('DB_USER', default='root'),
            password=config('DB_PASSWORD', default=''),
            db=config('DB_NAME', default='volapi')
        )
    except Exception as ex:
        Logger.add_to_log("Error", str(ex))
        Logger.add_to_log("Error", traceback.format_exc())