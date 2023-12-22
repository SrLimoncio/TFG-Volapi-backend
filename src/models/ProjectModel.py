# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler
# Exceptions
from src.utils.exceptions.exceptions import SQLExecutionError
from src.utils.exceptions.project_exceptions import (GenericProjectError,
                                                     NotValidInputsProjectError,
                                                     NotFoundProjectError,
                                                     DuplicateProjectError)

from src.utils.Logger import Logger
class ProjectModel:
    """
    Clase que encapsula información y operaciones relacionadas con proyectos en la base de datos.

    Methods:
        get_projects(cls, user_id):
            Recupera los proyectos asociados a un usuario desde la base de datos.

        get_project(cls, project_id):
            Obtiene información detallada sobre un proyecto dado su identificador.

        get_id_project_active(cls, user_id):
            Extrae el identificador del proyecto activo de un usuario.

        get_is_active_project(cls, project_id):
            Obtiene el estado de activación de un proyecto específico.

        activate_project(cls, id_project, user_id):
            Activa un proyecto y desactiva el resto para un usuario dado.

        create_project(cls, user_id, name, forensic_tool, memory_os, memory_path, sha256, sha1, md5):
            Crea un nuevo proyecto en la base de datos.

        update_name_project(cls, id_project, new_name):
            Actualiza el nombre de un proyecto existente.

        delete_project(cls, id_project):
            Elimina un proyecto de la base de datos.

    """

    @classmethod
    def get_projects(cls, user_id):
        """
        Recupera los proyectos del usuario de la base de datos.

        Args:
            user_id (int): ID del usuario.

        Returns:
            list: Lista de proyectos del usuario. Cada proyecto es una instancia de la clase ProjectModel.
                Retorna None si no hay proyectos o hay un error en la consulta.
        """
        query = "SELECT id, name, forensic_tool, memory_os, memory_path, sha256, sha1, md5, is_active FROM user_projects WHERE user_id = %s"
        values = (user_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return data if data else None

    @classmethod
    def get_id_project_active(cls, user_id):
        """
        Extrae el ID del proyecto activo de un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            int: ID del proyecto activo. Retorna None si no hay proyecto activo o hay un error en la consulta.
        """
        query = "SELECT id FROM user_projects WHERE user_id = %s AND is_active = 1"
        values = (user_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return data[0][0] if data else None

    @classmethod
    def get_project(cls, project_id):
        """
        Obtiene información sobre un proyecto a partir de su identificador.

        Args:
            project_id (int): ID del proyecto a consultar.

        Returns:
            dict: Diccionario con la información del proyecto.
                Retorna None si no se encuentra el proyecto o hay un error en la consulta.
        """
        query = f"SELECT id, name, forensic_tool, memory_os, memory_path FROM user_projects WHERE id = %s"
        values = (project_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return data[0] if data else None

    @classmethod
    def get_is_active_project(cls, project_id):
        """
        Obtener el estado de activación (is_active) de un proyecto específico.

        Args:
            project_id (int): ID del proyecto a consultar.

        Returns:
            bool: Estado de activación del proyecto (True si está activo, False si no está activo).
                Retorna None si no se encuentra el proyecto o hay un error en la consulta.
        """
        query = "SELECT is_active FROM user_projects WHERE id = %s"
        values = (project_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return data[0][0] if data else None

    @classmethod
    def activate_project(cls, id_project, user_id):
        """
        Pone un proyecto como activo y desactiva el resto.

        Args:
            id_project (int): ID del proyecto a activar.
            user_id (int): ID del usuario.

        Returns:
            bool: True si la operación fue exitosa, False si hay un error.
        """
        query = "UPDATE user_projects SET is_active = (id = %s) WHERE user_id = %s"
        values = (id_project, user_id)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.UPDATE)
        return True if data else False

    @classmethod
    def create_project(cls, user_id, name, forensic_tool, memory_os, memory_path, sha256, sha1, md5):
        """
        Crea un nuevo proyecto en la base de datos.

        Args:
            user_id (int): ID del usuario al que pertenece el proyecto.
            name (str): Nombre del proyecto.
            forensic_tool (int): Herramienta forense asociada al proyecto.
            memory_os (int): Sistema operativo de la memoria.
            memory_path (str): Ruta de la memoria.
            sha256 (str): Valor sha256 del proyecto.
            sha1 (str): Valor sha1 del proyecto.
            md5 (str): Valor md5 del proyecto.

        Returns:
            bool: True si la operación fue exitosa, False si hay un error.
        """
        try:
            name_procedure = "CreateProject"
            values = (user_id, name, forensic_tool, memory_os, memory_path, sha256, sha1, md5)
            data = DatabaseHandler.call_procedure(name_procedure, values)
            return True if data else False

        except SQLExecutionError as e:
            Logger.add_to_log("info", str("projectmodel:" + e))
            print("projectmodel:" + e)
            sqlstate = e.args[0]
            print("sqlstate: " + sqlstate)
            if sqlstate == '45000':
                raise GenericProjectError(f"Error SQL generico: {e}")
            elif sqlstate == '45001':
                raise NotValidInputsProjectError()
            elif sqlstate == '45002':
                raise DuplicateProjectError()
            elif sqlstate == '45003':
                raise NotFoundProjectError()
            else:
                raise GenericProjectError(f"Error SQL desconocido: {e}")

    @classmethod
    def update_name_project(cls, id_project, new_name):
        """
        Actualiza el nombre de un proyecto en la base de datos.

        Args:
            id_project (int): ID del proyecto a actualizar.
            new_name (str): Nuevo nombre para el proyecto.

        Returns:
            bool: True si la operación fue exitosa, False si hay un error.
        """
        query = "UPDATE user_projects SET name = %s WHERE id= %s"
        values = (new_name, id_project)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.UPDATE)
        return True if data else False

    @classmethod
    def delete_project(cls, id_project):
        """
        Elimina un proyecto de la base de datos.

        Args:
            id_project (int): ID del proyecto a eliminar.

        Returns:
            bool: True si la operación fue exitosa, False si hay un error.
        """
        query = "DELETE FROM user_projects WHERE id = %s"
        values = (id_project,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.DELETE)
        return True if data else False
