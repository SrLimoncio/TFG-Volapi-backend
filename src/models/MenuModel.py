
# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler


class MenuModel:
    @classmethod
    def get_categories(cls):
        """
        Recupera todas las categorías disponibles en la base de datos.

        Returns:
            list: Una lista de diccionarios con la información de cada categoría.
                  Cada diccionario contiene 'id', 'title' y 'description'.
                  Retorna None si no se encuentran categorías.
        """
        query = "SELECT id, title, description FROM vol3_categories ORDER BY display_order"
        data = DatabaseHandler.execute_query(query)
        return data if data else None

    @classmethod
    def get_commands_by_category(cls, category_id):
        """
        Obtiene los comandos asociados a una categoría específica.

        Args:
            category_id (int): ID de la categoría para la cual se obtienen los comandos.

        Returns:
            list: Una lista de diccionarios con la información de cada comando.
                  Cada diccionario contiene 'id', 'name', 'short_description', y 'plugin_options'.
                  Retorna None si no se encuentran comandos para la categoría.
        """
        #query = "SELECT id, title, description FROM menu_subcategories WHERE category_id = %s"
        #query = ("SELECT ms.id, vc.name, ms.description, ms.command_id FROM menu_subcategories_vol ms "
                 #"LEFT JOIN volatility_commands vc ON ms.command_id = vc.id WHERE ms.category_id = %s")
        query = "SELECT id, name, short_description, plugin_options FROM vol3_commands WHERE id_category = %s"
        values = (category_id,)
        data = DatabaseHandler.execute_query(query, values)
        return data if data else None

    @classmethod
    def get_status_command_user(cls, user_id, project_active, command_id):
        """
        Obtiene el estado actual de un comando para un usuario y proyecto específicos.

        Args:
            user_id (int): ID del usuario.
            project_active (int): ID del proyecto activo.
            command_id (int): ID del comando.

        Returns:
            str: El estado del comando. Retorna None si no se encuentra el estado.
        """
        query = ("SELECT state FROM vol3_user_state_commands "
                 "WHERE user_id = %s AND project_id = %s AND command_id = %s ")
        values = (user_id, project_active, command_id)
        data = DatabaseHandler.execute_query(query, values)
        return data[0][0] if data else None

    @classmethod
    def change_status_command(cls, user_id, command_id, project_active, new_status):
        """
        Cambia el estado de un comando para un usuario y proyecto específicos.

        Args:
            user_id (int): ID del usuario.
            command_id (int): ID del comando.
            project_active (int): ID del proyecto activo.
            new_status (str): Nuevo estado para el comando.

        Returns:
            bool: True si el cambio fue exitoso, False en caso contrario.
        """
        query = ("UPDATE vol3_user_state_commands SET state = %s "
                 "WHERE user_id = %s AND command_id = %s AND project_id = %s")
        values = (new_status, user_id, command_id, project_active)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.UPDATE)
