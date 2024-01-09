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
from src.utils.exceptions.error_handlers.SecurityErrorHandler import SecurityErrorHandler


class MenuCatService:
    @classmethod
    @SecurityErrorHandler.security_error_handler
    def get_menu_cats(cls, encoded_token):
        user_id = Security.verify_access_token(encoded_token)
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
                            "description": command[2],
                            "options": command[3]
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

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def get_info_subcat_user(cls, encoded_token, command_id):
        # Decodifica el token para obtener el usuario
        user_id = Security.verify_access_token(encoded_token)

        # Luego puedes usar el email del usuario para obtener las subcategorías correspondientes
        status = MenuModel.get_status_subcat_user(user_id, command_id)

        if status:
            return {"state": status, "success": True}, 200
        else:
            return {"state": None, "success": False}, 200
