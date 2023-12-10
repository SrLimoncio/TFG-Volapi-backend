import json
import traceback

# Database
from src.database.db_mysql import get_connection
# Logger
from src.utils.Logger import Logger


class DatabaseHandler:
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    @classmethod
    def execute_query(cls, sql_query, values=None, operation_type='SELECT'):
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
            else:
                connection.commit()  # Realizar commit para aplicar cambios en la base de datos
                result = None  # No hay resultados para consultas de inserción, actualización o eliminación

            cursor.close()
            connection.close()

            return result

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None
