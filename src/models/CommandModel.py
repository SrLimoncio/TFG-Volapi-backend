import json
from datetime import datetime
# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler
from src.utils.Logger import Logger


class CommandModel:
    """Clase para manejar información y operaciones relacionadas con comandos."""

    def __init__(self, _id, _name, _description, _parameters, _user_id, _result, _error, _execution_time):
        """Inicializa una instancia de la clase CommandModel."""
        self.id = _id
        self.name = _name
        self.description = _description
        self.parameters = _parameters
        self.user_id = _user_id
        self.result = _result
        self.error = _error
        self.execution_time = _execution_time

    @classmethod
    def get_info_command(cls, command_id):
        """Obtiene información sobre un comando."""
        query = "SELECT name, plugin_name, plugin_options, description, chart_type FROM vol3_commands WHERE id = %s"
        values = (command_id,)
        data = DatabaseHandler.execute_query(query, values)

        if data:
            command_dict = {
                'name': data[0][0],
                'plugin_name': data[0][1],
                'plugin_options': data[0][2],
                'description': data[0][3],
                'chart_type': data[0][4],
            }
            return command_dict
        else:
            return None

    @classmethod
    def create_result_vol_command(cls, command_id, user_id, project_id, result, command_line):
        """Guarda resultados de un comando para un usuario específico."""
        query = ("INSERT INTO results_commands_vol "
                 "(command_id, user_id, project_id, result, command_line) "
                 "VALUES (%s, %s, %s, %s, %s)")
        values = (command_id, user_id, project_id, result, command_line)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.INSERT)

    @classmethod
    def get_result_vol_command(cls, command_id, user_id, project_id):
        query = ("SELECT result, command_line, execution_time, error FROM results_commands_vol "
                 "WHERE command_id = %s AND user_id = %s AND project_id = %s")
        values = (command_id, user_id, project_id)
        data = DatabaseHandler.execute_query(query, values)

        if data:
            command_result_dict = {
                'result': data[0][0],
                'command_line': data[0][1],
                'execution_time': data[0][2],
                'error': data[0][3]
            }
            return command_result_dict
        else:
            return None

    @classmethod
    def delete_result_vol_command(cls, command_id, user_id, project_id):
        """
        Método para eliminar un resultado de comando de la base de datos.
        """
        query = ("DELETE FROM results_commands_vol "
                 "WHERE command_id = %s AND user_id = %s AND project_id = %s")
        values = (command_id, user_id, project_id)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.DELETE)

    @classmethod
    def result_to_json(cls, result):
        """
        """
        output_dict = {}

        # Dividimos las lineas de la salida
        rows = result.split("\n")
        # Quitamos las lineas en blanco
        data_rows = [row for row in rows if row.strip()]

        # Version de la salida
        version_row = data_rows[0]
        output_dict["version"] = version_row

        # Linea de la cabecera de la tabla
        header_row = data_rows[1]
        headers = header_row.split("\t")
        output_dict["headers"] = headers

        values_list = []
        for i in range(len(data_rows) - 2):
            # Valores de cada linea de la seccion de datos
            values = data_rows[i + 2].split("\t")
            # Creamos el diccionario de cada fila con la cabecera
            #data_dict = {headers[e]: values[e] for e in range(len(headers))}
            values_list.append(values)

        output_dict["values"] = values_list

        return output_dict
