# Esta clase se encarga de

# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler


class MenuModel:
    @classmethod
    def get_categories(cls):
        # Método para
        query = "SELECT id, title, description FROM vol3_categories ORDER BY display_order"
        data = DatabaseHandler.execute_query(query)
        return data if data else None

    @classmethod
    def get_commands_by_category(cls, category_id):
        # Método para
        #query = "SELECT id, title, description FROM menu_subcategories WHERE category_id = %s"
        #query = ("SELECT ms.id, vc.name, ms.description, ms.command_id FROM menu_subcategories_vol ms "
                 #"LEFT JOIN volatility_commands vc ON ms.command_id = vc.id WHERE ms.category_id = %s")
        query = "SELECT id, name, short_description FROM vol3_commands WHERE id_category = %s"
        values = (category_id,)
        data = DatabaseHandler.execute_query(query, values)
        return data if data else None

    @classmethod
    def get_status_command_user(cls, user_id, project_active, command_id):
        # Método para
        query = ("SELECT state FROM vol3_user_state_commands "
                 "WHERE user_id = %s AND project_id = %s AND command_id = %s ")
        values = (user_id, project_active, command_id)
        data = DatabaseHandler.execute_query(query, values)
        return data[0][0] if data else None

    @classmethod
    def change_status_command(cls, user_id, command_id, project_active, new_status):
        query = ("UPDATE vol3_user_state_commands SET state = %s "
                 "WHERE user_id = %s AND command_id = %s AND project_id = %s")
        values = (new_status, user_id, command_id, project_active)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.UPDATE)
