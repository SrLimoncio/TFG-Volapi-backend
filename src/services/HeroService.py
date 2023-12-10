import traceback

# Database
from src.database.db_mysql import get_connection
# Logger
from src.utils.Logger import Logger
# Models
# Hanadlers
from src.utils.FileHandler import FileHandler
from src.utils.DatabaseHandler import DatabaseHandler


class HeroServices():
    @classmethod
    def save_filepath(cls, token, pathfile):
        try:
            # 1. Comprobamos si el path es correcto
            file_is_correct = FileHandler.check_filepath(pathfile)

            if file_is_correct:
                # 1. Comprobamos si ya tiene token
                sql_query = "SELECT id_user FROM userbytoken WHERE id_token = %s"
                cursor.execute(sql_query, (token,))
                # Convertir la tupla en una lista de diccionarios
                data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]

                # Serializa el objeto JSON con UTF-8
                json_data = json.dumps(data, ensure_ascii=False, indent=4)
                DatabaseHandler.get_user_by_token()
                return token, True
            else:
                return "", False

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())