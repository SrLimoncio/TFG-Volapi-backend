# Esta clase se encarga de

# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler


class MenuModel:
    @classmethod
    def get_categories(cls):
        # Método para
        query = "SELECT id, title, description FROM menu_categories_vol"
        data = DatabaseHandler.execute_query(query)
        return data if data else None

    @classmethod
    def get_subcategories(cls, category_id):
        # Método para
        #query = "SELECT id, title, description FROM menu_subcategories WHERE category_id = %s"
        query = ("SELECT ms.id, vc.name, ms.description, ms.command_id FROM menu_subcategories_vol ms "
                 "LEFT JOIN volatility_commands vc ON ms.command_id = vc.id WHERE ms.category_id = %s")
        values = (category_id,)
        data = DatabaseHandler.execute_query(query, values)
        return data if data else None

    @classmethod
    def get_command_id_subcategory(cls, subcategory_id):
        # Método para
        #query = "SELECT id, title, description FROM menu_subcategories WHERE category_id = %s"
        query = ("SELECT command_id FROM menu_subcategories_vol WHERE id = %s")
        values = (subcategory_id,)
        data = DatabaseHandler.execute_query(query, values)
        return data[0][0] if data else None

    @classmethod
    def get_status_subcat_user(cls, user_id, subcategory_id, project_active):
        # Método para
        query = ("SELECT status FROM state_user_subcategories_vol "
                 "WHERE user_id = %s AND subcategory_id = %s AND project_id = %s")
        values = (user_id, subcategory_id, project_active)
        data = DatabaseHandler.execute_query(query, values)
        return data[0][0] if data else None

    @classmethod
    def change_status_command(cls, user_id, subcategory_id, project_active, new_status):
        query = ("UPDATE state_user_subcategories_vol SET status = %s "
                 "WHERE user_id = %s AND subcategory_id = %s AND project_id = %s")
        values = (new_status, user_id, subcategory_id, project_active)
        print("values state: " + str(user_id) + " " + str(subcategory_id) + " " + str(project_active) + " " + str(new_status))
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.UPDATE)
        print("data state:" + str(data))
