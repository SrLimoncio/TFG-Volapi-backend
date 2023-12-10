import traceback

# Security
from src.utils.Security import Security
# Models
from src.models.DashBoardModel import DashBoardModel

from src.utils.Logger import Logger


class DashBoardServices:
    @classmethod
    def get_projects_user(cls, encoded_token):
        try:
            decoded_token = Security.verify_token(encoded_token)
            if decoded_token:
                user_id = decoded_token['id']

                projects = DashBoardModel.get_projects(user_id)

                if projects:
                    projects_list = []
                    for project in projects:
                        category_dict = {
                            "id":       project[0],
                            "name":     project[1],
                            "tool":     project[2],
                            "os":       project[3],
                            "memory_path": project[4],
                            "sha256":   project[5],
                            "sha1":     project[6],
                            "md5":      project[7],
                            "state":    project[8]
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
