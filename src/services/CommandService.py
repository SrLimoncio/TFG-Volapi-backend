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
# Model
from src.models.CommandModel import CommandModel
from src.models.ProjectModel import ProjectModel
from src.models.UserModel import UserModel
from src.models.MenuModel import MenuModel


class CommandService:
    @classmethod
    def execute_volatility_command(cls, encoded_token, subcategory_id):
        try:
            # Decodifica el token para obtener el usuario
            payload_token = Security.verify_token(encoded_token)
            if payload_token:
                user_id = payload_token['id']
                project_id = UserModel.get_project_active(user_id)
                project = ProjectModel.get_project(project_id)
                tool = project.tool
                os = project.os
                memory_route = project.memory_path
                # Aqui deberiamos separar la logica entre windows/linux y vol2/vol3,
                # siempre pensando en una ampliacion
                command_id = MenuModel.get_command_id_subcategory(subcategory_id)
                command_data = CommandModel.get_info_command(command_id)
                command = command_data[0][0]
                parameters = command_data[0][1]

                # Luego puedes usar el email del usuario para obtener las subcategorías correspondientes
                output = Command.execute_command_windows(memory_route, command, parameters)

                result = output.stdout
                error = output.stderr

                if output.returncode == 0:
                    new_state = "active"
                    CommandModel.create_result_vol_command(command_id, user_id, project_id, result)
                    MenuModel.change_status_command(user_id, subcategory_id, project_id, new_state)
                    return {'message': 'OK', 'state': new_state, 'success': True}, 200
                else:
                    new_state = "inactive"
                    MenuModel.change_status_command(user_id, subcategory_id, project_id, new_state)
                    return {'message': 'ERROR', 'state': new_state, 'success': False}, 200

            else:
                # Devuelve un error si el token no es válido
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    def show_volatility_command(cls, encoded_token, subcategory_id):
        try:
            # Decodifica el token para obtener el usuario
            payload_token = Security.verify_token(encoded_token)
            if payload_token:
                user_id = payload_token['id']
                project_id = UserModel.get_project_active(user_id)
                command_id = MenuModel.get_command_id_subcategory(subcategory_id)
                command = CommandModel.get_info_command(command_id)
                command_title = command[0][0]
                command_description = command[0][2]
                result_data = CommandModel.get_result_vol_command(command_id, user_id, project_id)
                result = result_data[0]
                execution_time = result_data[1]
                error = result_data[2]
                result_json = CommandModel.result_to_json(result)
                print(result_json)

                return {'message': 'OK',
                        'title': command_title,
                        'description': command_description,
                        'command': command_title,
                        'commandOutput': result_json,
                        'success': True}, 200

            else:
                # Devuelve un error si el token no es válido
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

        """
        # 2. Comprobamos si ya se habia ejecutado el comando para dicho usuario
        first_execution = DatabaseHandler.check_if_cmd_has_execute(id_user, id_command)

        if not first_execution:
            cmd_result = 1
            # 3.1 Si no se habia ejecutado, lo ejecutamos y guardamos la salida en db
            # cmd_result = DatabaseHandler.execute_command()
        else:
            cmd_result = 0
            # 3.2 Si ya se habia ejecutado, sacamos el resultado de la db
            # cmd_result = DatabaseHandler.get_command()

        # 4. Convertimos el resultado a Json

        return cmd_result
        """




        #sql_query = '''SELECT EXISTS (SELECT 1 FROM WHERE )''', (cmd_name, parametres, cmd_result_decode)
        #result = DatabaseHandler.execute_query(sql_query)
        # Ejecutamos el comando de Volatility en terminal y obtenemos la salida
        #cmd = f"volatility -f {memory_dump_path} {cmd_name} {parametros}"
        #cmd_result = subprocess.check_output(cmd, shell=True)

        # Decodificar la salida en texto
        #cmd_result_decode = cmd_result.decode('utf-8')

        # Insertar el comando y el resultado en la base de datos
        #sql_query = '''INSERT INTO cmdlist * FROM infomenucat''', (cmd_name, parametres, cmd_result_decode)
        #result = DatabaseHandler.execute_query(sql_query)
        #return result
