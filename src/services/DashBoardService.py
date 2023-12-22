import traceback

# Security
from src.utils.Security import Security
# Models
from src.models.ProjectModel import ProjectModel
from src.utils.FileHandler import FileHandler

from src.utils.Logger import Logger


class DashBoardServices:
    @classmethod
    def get_projects_user(cls, encoded_token):
        try:
            decoded_token = Security.verify_token(encoded_token)
            if decoded_token:
                user_id = decoded_token['id']

                projects = ProjectModel.get_projects(user_id)

                if projects:
                    projects_list = []
                    for project in projects:
                        category_dict = {
                            "id":           project[0],
                            "name":         project[1],
                            "forensic_tool": project[2],
                            "memory_os":    project[3],
                            "memory_path":  project[4],
                            "sha256":       project[5],
                            "sha1":         project[6],
                            "md5":          project[7],
                            "is_active":    project[8]
                        }
                        projects_list.append(category_dict)

                    return {"projects": projects_list, "success": True}, 200
                else:
                    return {"projects": [], "success": False}, 200

            else:
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    def update_name_project(cls, encoded_token, id_project, new_name):
        try:
            decoded_token = Security.verify_token(encoded_token)
            if decoded_token:
                user_id = decoded_token['id']

                ProjectModel.update_name_project(id_project, new_name)

                return {"projects": "projects_list", "success": True}, 200

            else:
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    def update_active_project(cls, encoded_token, id_project):
        try:
            decoded_token = Security.verify_token(encoded_token)
            if decoded_token:
                user_id = decoded_token['id']

                ProjectModel.activate_project(id_project, user_id)

                return {"message": "ok", "success": True}, 200

            else:
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500

    @classmethod
    def create_project(cls, encoded_token, name, tool, os, memory_path):
        try:
            decoded_token = Security.verify_token(encoded_token)
            if decoded_token:
                user_id = decoded_token['id']

                sha256, sha1, md5 = FileHandler.calculate_hashes(memory_path)

                success = ProjectModel.create_project(user_id, name, tool, os, memory_path, sha256, sha1, md5)

                return {"message": "OK", "success": True}, 200

            else:
                return {'message': 'Token de autorización no válido', 'success': False}, 401

        except Exception as ex:
            print(ex)
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'message': "Error interno", 'success': False}, 500