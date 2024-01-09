import json
import traceback
import pymysql

# Database
from src.database.db_mysql import get_connection
# Logger
from src.utils.Logger import Logger
# Exceptions
from src.utils.exceptions.CustomExceptions import SQLCustomException


class DatabaseHandler:
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    @classmethod
    def execute_query(cls, sql_query, values=None, operation_type='SELECT'):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            if connection is None:
                return None

            cursor = connection.cursor()

            if values:
                cursor.execute(sql_query, values)
            else:
                cursor.execute(sql_query)

            if operation_type == 'SELECT':
                result = cursor.fetchall()

            elif operation_type in ['INSERT', 'UPDATE', 'DELETE']:
                affected_rows = cursor.rowcount
                connection.commit()
                result = f"{affected_rows} filas afectadas."

            else:
                result = None  # Operación desconocida

            return result

        finally:
            # Asegurarse de cerrar el cursor y la conexión incluso si ocurre una excepción
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def call_procedure(cls, name_procedure, parameters):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            if connection is None:
                return None

            cursor = connection.cursor()

            # Llamar al procedimiento almacenado
            cursor.callproc(name_procedure, parameters)

            results = cursor.fetchall()
            connection.commit()

            return results

        except pymysql.err.InternalError as e:
            Logger.add_to_log("info", str("DatabaseHandler:" + e))
            print("DatabaseHandler:" + e)
            raise SQLCustomException(f"Error SQL: {e}")

        finally:
            # Cerramos el cursor y la conexión incluso si ocurre una excepción
            if cursor:
                cursor.close()
            if connection:
                connection.close()
