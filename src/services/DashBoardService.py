import traceback

# Security
from src.utils.Security import Security
# Models
from src.models.ProjectModel import ProjectModel
from src.utils.FileHandler import FileHandler

from src.utils.Logger import Logger
from src.utils.exceptions.error_handlers.SecurityErrorHandler import SecurityErrorHandler


class DashBoardServices:
    @classmethod
    @SecurityErrorHandler.security_error_handler
    def user_has_projects(cls, encoded_token):
        try:
            user_id = Security.verify_access_token(encoded_token)

            has_project = ProjectModel.has_project_active(user_id)

            return {"hasProject": has_project, "success": True}, 201

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def get_projects_user(cls, encoded_token):
        try:
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

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def update_name_project(cls, encoded_token, id_project, new_name):
        try:
            user_id = Security.verify_access_token(encoded_token)

            ProjectModel.update_name_project(id_project, new_name)

            return {"projects": "projects_list", "success": True}, 200

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def update_active_project(cls, encoded_token, id_project):
        try:
            user_id = Security.verify_access_token(encoded_token)

            ProjectModel.activate_project(id_project, user_id)

            return {"message": "ok", "success": True}, 200

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def create_project(cls, encoded_token, name, tool, os):
        try:
            user_id = Security.verify_access_token(encoded_token)

            project_id = ProjectModel.create_project(user_id, name, tool, os)

            return {"message": "OK", "projectId": project_id, "success": True}, 200

        except Exception as ex:
            print(ex)
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def upload_chunk_file(cls, encoded_token, project_id, chunk, chunk_number, _total_chunks, _file_name):
        try:
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
                Logger.add_to_log("info", "memory_name")
                Logger.add_to_log("info", memory_name)

                project_id = ProjectModel.update_memory_info_project(project_id, memory_name, sha256, sha1, md5)

                return {"message": "OK", "success": True}, 200

            return {"message": "OK", "success": True}, 200

        except Exception as ex:
            print(ex)
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    @SecurityErrorHandler.security_error_handler
    def delete_project(cls, encoded_token, project_id):
        try:
            user_id = Security.verify_access_token(encoded_token)

            success = ProjectModel.delete_project(user_id, project_id)

            return {"message": "OK", "success": True}, 200

        except Exception as ex:
            print(ex)
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500
