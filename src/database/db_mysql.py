from decouple import config
import pymysql

# Exceptions
from src.exceptions.DataBaseExceptions import DBConnectionException


def get_connection():
    try:
        return pymysql.connect(
            host=config('DB_HOST', default='localhost'),
            user=config('DB_USER', default='root'),
            password=config('DB_PASSWORD', default=''),
            db=config('DB_NAME', default='volapi_develop')
        )

    except Exception as ex:
        raise DBConnectionException(f"Error SQL: Conexion fallida con la Base de datos: {ex}")
