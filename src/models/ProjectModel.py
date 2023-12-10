# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler


class ProjectModel:
    """Clase para manejar información y operaciones relacionadas con proyectos."""

    def __init__(self, _id, _name, _tool, _os, _memory_path):
        """Inicializa una instancia de Projecto."""
        self.id = _id
        self.name = _name
        self.tool = _tool
        self.os = _os
        self.memory_path = _memory_path

    @classmethod
    def get_project(cls, project_id):
        """Obtiene información sobre un proyecto a partir de su identificador."""
        query = f"SELECT id, name, tool, os, memory_path FROM projects WHERE id = %s"
        values = (project_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return cls(*data[0]) if data else None
