import traceback

# DatabaseHandler
from src.utils.DatabaseHandler import DatabaseHandler
# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Model
from src.models.MenuModel import MenuModel
from src.models.UserModel import UserModel
from src.models.ProjectModel import ProjectModel


class MenuCatService():
    @classmethod
    def get_menu_cats(cls, encoded_token):
        try:
            decoded_token = Security.verify_token(encoded_token)
            if decoded_token:
                user_id = decoded_token['id']
                project_active = ProjectModel.get_id_project_active(user_id)
                categories_data = MenuModel.get_categories()

                if categories_data:
                    # Convertir los datos de categorías a un formato adecuado
                    categories_list = []

                    for category in categories_data:
                        category_id = category[0]
                        category_dict = {
                            "id": category_id,
                            "title": category[1],
                            "description": category[2]
                        }

                        # Obtener subcategorías para la categoría actual
                        commands_data = MenuModel.get_commands_by_category(category_id)

                        if commands_data:
                            commands_list = []

                            for command in commands_data:
                                command_id = command[0]
                                commands_dict = {
                                    "id": command_id,
                                    "title": command[1],
                                    "description": command[2]
                                }

                                # Obtener información adicional sobre el estado de la subcategoría
                                status = MenuModel.get_status_command_user(user_id, project_active, command_id)

                                commands_dict["state"] = status

                                commands_list.append(commands_dict)

                            category_dict["commands"] = commands_list

                        categories_list.append(category_dict)

                    return {"categories": categories_list, "success": True}, 200
                else:
                    return {"categories": [], "success": False}, 200
            else:
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    def get_info_subcat_user(cls, encoded_token, command_id):
        try:
            # Decodifica el token para obtener el usuario
            decoded_token = Security.verify_token(encoded_token)
            if decoded_token:
                user_id = decoded_token['id']

                # Luego puedes usar el email del usuario para obtener las subcategorías correspondientes
                status = MenuModel.get_status_subcat_user(user_id, command_id)

                if status:
                    return {"state": status, "success": True}, 200
                else:
                    return {"state": None, "success": False}, 200
            else:
                # Devuelve un error si el token no es válido
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500
