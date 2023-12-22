import traceback

from click import command

# DatabaseHandler
from src.utils.DatabaseHandler import DatabaseHandler
# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# CommandUtils
from src.utils.Command import Command
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
    def execute_volatility_command(cls, encoded_token, command_id):
        try:
            # Decodifica el token para obtener el usuario
            payload_token = Security.verify_token(encoded_token)
            if payload_token:
                user_id = payload_token['id']
                project_id = ProjectModel.get_id_project_active(user_id)
                project = ProjectModel.get_project(project_id)
                tool = project[2]
                os = project[3]
                memory_route = project[4]
                # Aqui deberiamos separar la logica entre windows/linux y vol2/vol3,
                # siempre pensando en una ampliacion
                command_data = CommandModel.get_info_command(command_id)
                # name
                # plugin_name
                # plugin_options
                # description
                plugin_name = command_data[1]
                plugin_options = command_data[2]

                # Obtener el executor utilizando la la fábrica de estrategias
                executor = CommandFactory().get_executor(os, tool)

                # Ejecutar el comando
                output, output_command = executor.execute_command(memory_route, plugin_name, plugin_options)
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

            else:
                # Devuelve un error si el token no es válido
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    def show_volatility_command(cls, encoded_token, command_id):
        try:
            # Decodifica el token para obtener el usuario
            payload_token = Security.verify_token(encoded_token)
            if payload_token:
                user_id = payload_token['id']
                project_id = ProjectModel.get_id_project_active(user_id)
                command = CommandModel.get_info_command(command_id)
                # name, plugin_name, plugin_options, description, chart_type
                command_name = command[0]
                command_description = command[3]
                chart_type = command[4]
                print(chart_type)

                result_data = CommandModel.get_result_vol_command(command_id, user_id, project_id)
                # result, command_line, execution_time, error
                result = result_data[0]
                command_line = result_data[1]
                execution_time = result_data[2]
                error = result_data[3]

                result_json = CommandModel.result_to_json(result)
                Logger.add_to_log("info", result_json['values'])

                chart_json = None
                if chart_type:
                    # Obtener el chart_builder utilizando la la fábrica de estrategias
                    chart_builder = ChartFactory().get_builder(chart_type)

                    # Crear el chart
                    chart_json = chart_builder.build_chart(result_json)

                Logger.add_to_log("info", "chjart")
                Logger.add_to_log("info", chart_json)

                return {'message': 'OK',
                        'title': command_name,
                        'description': command_description,
                        'command_line': command_line,
                        'execution_time': execution_time,
                        'commandOutput': result_json,
                        'chartOutput': chart_json,
                        'success': True}, 200

            else:
                # Devuelve un error si el token no es válido
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500
