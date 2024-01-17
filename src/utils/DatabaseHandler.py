import pymysql

# Database
from src.database.db_mysql import get_connection
# Logger
# from src.utils.Logger import Logger
# Exceptions
from src.exceptions.DataBaseExceptions import (DBOperationException,
                                               DBConnectionException,
                                               InvalidQueryException,
                                               DBProcedureException)


class DatabaseHandler:
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    @classmethod
    def execute_query(cls, sql_query, values=None, operation_type='SELECT'):
        """
        Ejecuta una consulta SQL en la base de datos.

        Args:
            sql_query (str): Consulta SQL a ejecutar.
            values (tuple, optional): Valores a pasar a la consulta.
            operation_type (str): Tipo de operación (SELECT, INSERT, UPDATE, DELETE).

        Returns:
            varied: Resultado de la consulta.

        Raises:
            DBConnectionException: Si falla la conexión con la base de datos.
            InvalidQueryException: Si el tipo de operación es desconocido.
            DBOperationException: Si ocurre un error en la operación de la base de datos.
        """

        connection = None
        cursor = None
        try:
            connection = get_connection()
            if connection is None:
                raise DBConnectionException(f"Error SQL: Conexion fallida con la Base de datos.")

            cursor = connection.cursor()

            if values:
                cursor.execute(sql_query, values)
            else:
                cursor.execute(sql_query)

            if operation_type == 'SELECT':
                result = cursor.fetchall()
            elif operation_type in ['INSERT', 'UPDATE', 'DELETE']:
                connection.commit()
                result = f"{cursor.rowcount} filas afectadas."

            else:
                raise InvalidQueryException("Error SQL: Tipo de operacion desconocida")

            return result

        except pymysql.Error as e:
            raise DBOperationException(f"Error SQL: Operacion sql fallida: {e}")

        finally:
            # Asegurarse de cerrar el cursor y la conexión incluso si ocurre una excepción
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def call_procedure(cls, name_procedure, parameters):
        """
        Llama a un procedimiento almacenado en la base de datos.

        Args:
            name_procedure (str): Nombre del procedimiento almacenado.
            parameters (tuple): Parámetros a pasar al procedimiento.

        Returns:
            list: Resultados del procedimiento almacenado.

        Raises:
            DBConnectionException: Si falla la conexión con la base de datos.
            DBProcedureException: Si falla la ejecución del procedimiento almacenado.
            DBOperationException: Si ocurre un error en la operación de la base de datos.
        """

        connection = None
        cursor = None
        try:
            connection = get_connection()
            if connection is None:
                raise DBConnectionException(f"Error SQL: Conexion fallida con la Base de datos.")

            cursor = connection.cursor()

            # Llamar al procedimiento almacenado
            cursor.callproc(name_procedure, parameters)

            results = cursor.fetchall()
            connection.commit()

            return results

        except pymysql.MySQLError as e:
            if e.args[0] == 1644:
                raise DBProcedureException(e.args[1])
            else:
                raise DBOperationException(f"Error SQL: Operacion procedure fallida: {e}")

        finally:
            # Cerramos el cursor y la conexión incluso si ocurre una excepción
            if cursor:
                cursor.close()
            if connection:
                connection.close()
