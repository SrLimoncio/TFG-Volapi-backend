# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler
# Exceptions
from src.exceptions.ProjectExceptions import (SQLCustomException,
                                              GenericProjectCustom,
                                              NotValidInputsProjectCustom,
                                              NotFoundProjectCustom,
                                              DuplicateProjectCustom)


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
    def has_project_active(cls, user_id):
        """
        Comprueba si el usuario tiene proyectos activos.

        Args:
            user_id (int): ID del usuario.

        Returns:
            bool: True si el usuario tiene al menos un proyecto activo, False en caso contrario.
        """
        query = "SELECT 1 FROM user_projects WHERE user_id = %s AND is_active = TRUE LIMIT 1"
        values = (user_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        # Devuelve True si se encuentra al menos un proyecto activo, False en caso contrario
        return bool(data)

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
        query = "SELECT id, name, forensic_tool, memory_os, memory_file, sha256, sha1, md5, is_active FROM user_projects WHERE user_id = %s"
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
        query = "SELECT id, name, forensic_tool, memory_os, memory_file FROM user_projects WHERE id = %s"
        values = (project_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)

        if data:
            project_dict = {
                'id': data[0][0],
                'name': data[0][1],
                'tool': data[0][2],
                'os': data[0][3],
                'memory_file': data[0][4]
            }
            return project_dict
        else:
            return None

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
    def create_project(cls, user_id, name, forensic_tool, memory_os):
        """
        Crea un nuevo proyecto en la base de datos.

        Args:
            user_id (int): ID del usuario al que pertenece el proyecto.
            name (str): Nombre del proyecto.
            forensic_tool (int): Herramienta forense asociada al proyecto.
            memory_os (int): Sistema operativo de la memoria.

        Returns:
            bool: True si la operación fue exitosa, False si hay un error.
        """
        try:
            name_procedure = "CreateProject"
            values = (user_id, name, forensic_tool, memory_os)
            data = DatabaseHandler.call_procedure(name_procedure, values)
            return data if data else None

        except SQLCustomException as e:
            if e.message == 'Error: Parámetros de entrada no válidos':
                raise NotValidInputsProjectCustom()
            elif e.message == 'Error: Ya existe un proyecto con ese nombre':
                raise DuplicateProjectCustom()
            elif e.message == 'Error: No se pudo obtener el ID del proyecto recién insertado':
                raise NotFoundProjectCustom()
            else:
                raise GenericProjectCustom(f"Error SQL no controlado: {e}")

    @classmethod
    def update_memory_info_project(cls, project_id, memory_path, sha256, sha1, md5):
        """
        Actualiza la información de memoria de un proyecto.

        Args:
            project_id (int): ID del proyecto a actualizar.
            memory_path (str): Ruta del archivo de memoria.
            sha256 (str): Hash SHA256 del archivo de memoria.
            sha1 (str): Hash SHA1 del archivo de memoria.
            md5 (str): Hash MD5 del archivo de memoria.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        query = ("UPDATE user_projects "
                 "SET memory_file = %s , sha256 = %s , sha1 = %s , md5 = %s "
                 "WHERE id= %s")
        values = (memory_path, sha256, sha1, md5, project_id)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.UPDATE)
        return True if data else False

    @classmethod
    def push_upload_info_project(cls, project_id, total_chunks, _file_name):
        """
        Inserta información sobre la carga de un archivo en la base de datos.

        Args:
            project_id (int): ID del proyecto asociado.
            total_chunks (int): Número total de fragmentos del archivo.
            _file_name (str): Nombre del archivo.

        No retorna nada.
        """
        query = ("INSERT INTO user_project_info_upload_file "
                 "(project_id, total_chunks, file_name) "
                 "VALUES ( %s, %s, %s )")
        values = (project_id, total_chunks, _file_name)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.INSERT)

    @classmethod
    def get_upload_info_project(cls, project_id):
        """
        Recupera información sobre la carga de un archivo para un proyecto.

        Args:
            project_id (int): ID del proyecto a consultar.

        Returns:
            tuple: Contiene el número total de fragmentos y el nombre del archivo, si existe.
                   Retorna None si no hay datos o hay un error en la consulta.
        """
        query = "SELECT total_chunks, file_name FROM user_project_info_upload_file WHERE project_id = %s"
        values = (project_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return data[0] if data else None

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
    def delete_project(cls, id_user, id_project):
        """
        Elimina un proyecto de la base de datos.

        Args:
            id_project (int): ID del proyecto a eliminar.

        Returns:
            bool: True si la operación fue exitosa, False si hay un error.
        """
        try:
            name_procedure = "DeleteProject"
            values = (id_user, id_project)
            data = DatabaseHandler.call_procedure(name_procedure, values)
            return data[-1][0] if data else None

        except SQLCustomException as e:
            sqlstate = e.args[0]
            if sqlstate == '45000':
                raise GenericProjectCustom(f"Error SQL generico: {e}")
            else:
                raise GenericProjectCustom(f"Error SQL desconocido: {e}")
