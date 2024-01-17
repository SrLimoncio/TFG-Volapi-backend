from src.models.UserModel import UserModel
# Security
from src.utils.Security import Security
# Models
from src.models.ProjectModel import ProjectModel
from src.utils.FileHandler import FileHandler


class DashBoardServices:
    @classmethod
    def user_has_projects(cls, encoded_token):
        """
        Verifica si un usuario tiene proyectos activos.

        Args:
            encoded_token (str): Token de acceso codificado del usuario.

        Returns:
            dict: Un diccionario indicando si el usuario tiene proyectos activos y un código de estado HTTP.
        """
        user_id = Security.verify_access_token(encoded_token)

        has_project = ProjectModel.has_project_active(user_id)

        return {"hasProject": has_project, "success": True}, 200

    @classmethod
    def get_projects_user(cls, encoded_token):
        """
        Obtiene los proyectos asociados a un usuario.

        Args:
            encoded_token (str): Token de acceso codificado del usuario.

        Returns:
            dict: Un diccionario con la lista de proyectos del usuario y un código de estado HTTP.
        """
        user_id = Security.verify_access_token(encoded_token)

        projects = ProjectModel.get_projects(user_id)

        if projects:
            projects_list = []
            for project in projects:
                memory_file_name = project[4].split("\\")[-1]
                category_dict = {
                    "id":           project[0],
                    "name":         project[1],
                    "forensic_tool": project[2],
                    "memory_os":    project[3],
                    "memory_name":  memory_file_name,
                    "sha256":       project[5],
                    "sha1":         project[6],
                    "md5":          project[7],
                    "is_active":    project[8]
                }
                projects_list.append(category_dict)

            return {"projects": projects_list, "success": True}, 200
        else:
            return {"projects": [], "success": False}, 200

    @classmethod
    def update_name_project(cls, encoded_token, id_project, new_name):
        """
        Actualiza el nombre de un proyecto específico.

        Args:
            encoded_token (str): Token de acceso codificado del usuario.
            id_project (int): ID del proyecto a actualizar.
            new_name (str): Nuevo nombre para el proyecto.

        Returns:
            dict: Un mensaje de éxito y un código de estado HTTP.
        """
        user_id = Security.verify_access_token(encoded_token)

        projects = ProjectModel.get_projects(user_id)

        if projects:
            for project in projects:
                if new_name == project[1]:
                    return {'message': "Conflict", 'success': False}, 409

        ProjectModel.update_name_project(id_project, new_name)

        return {"message": "OK", "success": True}, 200

    @classmethod
    def update_active_project(cls, encoded_token, id_project):
        """
        Activa un proyecto específico.

        Args:
            encoded_token (str): Token de acceso codificado del usuario.
            id_project (int): ID del proyecto a activar.

        Returns:
            dict: Un mensaje de éxito y un código de estado HTTP.
        """
        user_id = Security.verify_access_token(encoded_token)

        ProjectModel.activate_project(id_project, user_id)

        return {"message": "ok", "success": True}, 200

    @classmethod
    def create_project(cls, encoded_token, name, tool, os):
        """
        Crea un nuevo proyecto.

        Args:
            encoded_token (str): Token de acceso codificado del usuario.
            name (str): Nombre del proyecto.
            tool (str): Herramienta asociada al proyecto.
            os (str): Sistema operativo del proyecto.

        Returns:
            dict: Un mensaje de éxito, el ID del proyecto creado y un código de estado HTTP.
        """
        user_id = Security.verify_access_token(encoded_token)

        project_id = ProjectModel.create_project(user_id, name, tool, os)

        return {"message": "OK", "projectId": project_id, "success": True}, 200

    @classmethod
    def upload_chunk_file(cls, encoded_token, project_id, chunk, chunk_number, _total_chunks, _file_name):
        """
        Maneja la carga de fragmentos de un archivo para un proyecto.

        Args:
            encoded_token (str): Token de acceso codificado del usuario.
            project_id (int): ID del proyecto.
            chunk (File): Fragmento del archivo a cargar.
            chunk_number (int): Número del fragmento.
            _total_chunks (int): Número total de fragmentos.
            _file_name (str): Nombre del archivo.

        Returns:
            dict: Un mensaje de éxito y un código de estado HTTP.
        """
        user_id = Security.verify_access_token(encoded_token)

        total_chunks = 0
        if _total_chunks and _file_name:
            ProjectModel.push_upload_info_project(project_id, _total_chunks, _file_name)
            total_chunks = _total_chunks
            file_name = _file_name
        else:
            data_info_chunks = ProjectModel.get_upload_info_project(project_id)
            total_chunks = data_info_chunks[0]
            file_name = data_info_chunks[1]

        FileHandler.save_chunk_temporal_path(user_id, project_id, chunk, chunk_number)

        # Lógica para verificar si todos los trozos han llegado
        if FileHandler.check_all_chunks_received(user_id, project_id, total_chunks):
            # Reensamblar el archivo
            final_file_path = FileHandler.reassemble_file(user_id, project_id, file_name)

            # Realizar acciones finales, como calcular hashes y actualizar la base de datos
            #memory_temporal_path = FileHandler.save_and_check_image_file(memory_file, user_id, name)

            sha256, sha1, md5 = FileHandler.calculate_hashes(final_file_path)

            memory_name = final_file_path.split("\\")[-1]

            project_id = ProjectModel.update_memory_info_project(project_id, memory_name, sha256, sha1, md5)

            return {"message": "OK", "success": True}, 200

        return {"message": "OK", "success": True}, 200

    @classmethod
    def delete_project(cls, encoded_token, project_id):
        """
        Elimina un proyecto específico.

        Args:
            encoded_token (str): Token de acceso codificado del usuario.
            project_id (int): ID del proyecto a eliminar.

        Returns:
            dict: Un mensaje de éxito y un código de estado HTTP.
        """
        user_id = Security.verify_access_token(encoded_token)
        project_active = ProjectModel.get_id_project_active(user_id)

        if project_active == project_id :
            return {"message": "It is not possible to delete the active project", "success": False}, 409

        success = ProjectModel.delete_project(user_id, project_id)

        return {"message": "OK", "success": True}, 200

    @classmethod
    def get_profile_user(cls, encoded_token):
        user_id = Security.verify_access_token(encoded_token)

        profile = UserModel.get_profile(user_id)

        if profile:
            profile_dict = {
                "name": profile[0],
                "email": profile[1],
                "username": profile[2],
                "datacreation": profile[3]
            }
            return {"profile": profile_dict, "success": True}, 200
        else:
            return {"projects": [], "success": False}, 200
