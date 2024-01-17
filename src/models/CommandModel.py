# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler


class CommandModel:
    """Clase para manejar información y operaciones relacionadas con comandos."""

    @classmethod
    def create_result_vol_command(cls, command_id, user_id, project_id, result, command_line):
        """
        Guarda resultados de un comando para un usuario específico.

        Args:
            command_id (int): Identificador del comando.
            user_id (int): Identificador del usuario.
            project_id (int): Identificador del proyecto.
            result (str): Resultado del comando.
            command_line (str): Línea de comando ejecutada.
        """
        query = ("INSERT INTO results_commands_vol "
                 "(command_id, user_id, project_id, result, command_line) "
                 "VALUES (%s, %s, %s, %s, %s)")
        values = (command_id, user_id, project_id, result, command_line)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.INSERT)

    @classmethod
    def get_info_command(cls, command_id):
        """
        Obtiene información sobre un comando.

        Args:
            command_id (int): Identificador del comando.

        Returns:
            Optional[Dict[str, str]]: Diccionario con la información del comando si se encuentra, None en caso contrario.
        """

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
    def get_result_vol_command(cls, command_id, user_id, project_id):
        """
        Obtiene el resultado de un comando para un usuario y proyecto específicos.

        Args:
            command_id (int): Identificador del comando.
            user_id (int): Identificador del usuario.
            project_id (int): Identificador del proyecto.

        Returns:
            Optional[Dict[str, str]]: Diccionario con el resultado del comando si se encuentra, None en caso contrario.
        """
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
        Elimina un resultado de comando de la base de datos para un usuario y proyecto específicos.

        Args:
            command_id (int): Identificador del comando.
            user_id (int): Identificador del usuario.
            project_id (int): Identificador del proyecto.
        """
        query = ("DELETE FROM results_commands_vol "
                 "WHERE command_id = %s AND user_id = %s AND project_id = %s")
        values = (command_id, user_id, project_id)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.DELETE)

    @classmethod
    def result_to_json(cls, result):
        """
        Convierte el resultado de un comando a formato JSON.

        Args:
            result (str): Resultado del comando en formato de texto.

        Returns:
            Dict[str, List[str]]: Diccionario que representa el resultado en formato JSON.
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
