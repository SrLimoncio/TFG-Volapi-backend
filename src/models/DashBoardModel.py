
# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler
# UserModel
from src.models.UserModel import UserModel

from src.utils.Logger import Logger


class DashBoardModel:
    """
    def __init__(self, _id, _name, _tool, _os, _memory_path, _sha256, _sha1, _md5, _state):
        self.id = _id
        self.name = _name
        self.tool = _tool
        self.os = _os
        self.memory_path = _memory_path
        self.sha256 = _sha256
        self.sha1 = _sha1
        self.md5 = _md5
        self.state = _state
    """

    @classmethod
    def get_projects(cls, user_id):
        # Método para recuperar los proyectos del usuario de la base de datos
        query = "SELECT id, name, tool, os, memory_path, sha256, sha1, md5, state FROM projects WHERE user_id = %s"
        values = (user_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return data if data else None
