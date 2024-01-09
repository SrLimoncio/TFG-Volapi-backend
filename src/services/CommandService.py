import traceback
import json

from click import command

# Handlers
from src.utils.DatabaseHandler import DatabaseHandler
from src.utils.FileHandler import FileHandler
# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# CommandUtils
from src.services.command.CommandStrategy import CommandFactory
from src.services.command.CommandExecutor import CommandExecutor
from src.services.charts.ChartStrategy import ChartFactory
from src.services.charts.ChartBuilder import ChartBuilder
# Model
from src.models.CommandModel import CommandModel
from src.models.ProjectModel import ProjectModel
from src.models.UserModel import UserModel
from src.models.MenuModel import MenuModel


class CommandService:
    @classmethod
    def execute_volatility_command(cls, encoded_token, command_id, user_cmd_options):
        try:
            # Decodifica el token para obtener el usuario
            user_id = Security.verify_access_token(encoded_token)

            project_id = ProjectModel.get_id_project_active(user_id)

            # project_dict -> 'id', 'name', 'tool', 'os', 'memory_file'
            project_dict = ProjectModel.get_project(project_id)

            # command_dict -> 'name', 'plugin_name', 'plugin_options', 'description', 'chart_type'
            command_dict = CommandModel.get_info_command(command_id)

            command_options = None
            if command_dict['plugin_options'] and user_cmd_options:
                plugin_options = json.loads(command_dict['plugin_options'])

                command_options = []
                for option in plugin_options:
                    option_id = option['id']
                    if option_id in user_cmd_options:
                        command_options.append(
                            {'code': option['code'],
                             'type': option['type'],
                             'value': user_cmd_options[option_id]
                             })

            memory_file_path = FileHandler.generate_path_memory_file(user_id,
                                                                     project_id,
                                                                     project_dict['memory_file'])

            # Obtener el executor utilizando la fábrica de estrategias
            executor = CommandFactory().get_executor(project_dict['os'],
                                                     project_dict['tool'])
            # Ejecutar el comando
            output, output_command = executor.execute_command(memory_file_path,
                                                              command_dict['plugin_name'],
                                                              command_options)
            # output = Command.execute_command_windows(memory_route, command, parameters)

            result = output.stdout
            error = output.stderr

            if output.returncode == 0:
                new_state = "active"
                CommandModel.create_result_vol_command(command_id, user_id, project_id, result, output_command)
                MenuModel.change_status_command(user_id, command_id, project_id, new_state)
                return {'message': 'OK', 'state': new_state, 'success': True}, 200
            else:
                new_state = "inactive"
                MenuModel.change_status_command(user_id, command_id, project_id, new_state)
                return {'message': 'ERROR', 'state': new_state, 'success': False}, 200

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    def show_volatility_command(cls, encoded_token, command_id):
        try:
            # Decodifica el token para obtener el usuario
            user_id = Security.verify_access_token(encoded_token)

            project_id = ProjectModel.get_id_project_active(user_id)

            # command_dict -> 'name', 'plugin_name', 'plugin_options', 'description', 'chart_type'
            command_dict = CommandModel.get_info_command(command_id)

            # command_dict -> 'result', 'command_line', 'execution_time', 'error'
            command_result_dict = CommandModel.get_result_vol_command(command_id, user_id, project_id)

            result_json = CommandModel.result_to_json(command_result_dict['result'])

            chart_json = None
            if command_dict['chart_type']:
                # Obtener el chart_builder utilizando la la fábrica de estrategias
                chart_builder = ChartFactory().get_builder(command_dict['chart_type'], command_id)
                # Crear el chart
                chart_json = chart_builder.build_chart(command_id, result_json)

            return {'message': 'OK',
                    'title': command_dict['name'],
                    'description': command_dict['description'],
                    'command_line': command_result_dict['command_line'],
                    'execution_time': command_result_dict['execution_time'],
                    'commandOutput': result_json,
                    'chartOutput': chart_json,
                    'success': True}, 200

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    def delete_result_command(cls, encoded_token, command_id):
        try:
            # Decodifica el token para obtener el usuario
            user_id = Security.verify_access_token(encoded_token)

            project_id = ProjectModel.get_id_project_active(user_id)

            CommandModel.delete_result_vol_command(command_id, user_id, project_id)

            return {'message': 'OK', 'state': 'inactive', 'success': True}, 200

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': 'Token de autorización no válido', 'success': False}, 401
            return {'message': "Error interno", 'success': False}, 500
