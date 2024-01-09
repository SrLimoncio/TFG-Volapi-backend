import traceback
import os
import hashlib
from werkzeug.utils import secure_filename

# Logger
from src.utils.Logger import Logger


class FileHandler:
    # Define la ruta base de la carpeta userfiles
    BASE_UPLOAD_FOLDER = 'UserFiles'

    @classmethod
    def generate_path_memory_file(cls, user_id, project_id, file_name):
        try:
            upload_folder = os.path.join(cls.BASE_UPLOAD_FOLDER, "user_" + str(user_id),
                                         "project_" + str(project_id), "memory_file", file_name)

            return upload_folder

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def save_chunk_temporal_path(cls, user_id, project_id, chunk, chunk_number):
        try:
            filename = secure_filename(f"project_{project_id}_chunk_{chunk_number}.tmp")
            upload_folder = os.path.join(cls.BASE_UPLOAD_FOLDER, "user_" + str(user_id),
                                     "project_" + str(project_id), "temporal_chunks")
            os.makedirs(upload_folder, exist_ok=True)

            save_path = os.path.join(upload_folder, filename)
            chunk.save(save_path)

            return True

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def check_all_chunks_received(cls, user_id, project_id, total_chunks):
        try:
            # Contar los archivos temporales de trozos que se han guardado
            chunks_path = os.path.join(cls.BASE_UPLOAD_FOLDER, f"user_{user_id}",
                                       f"project_{project_id}", "temporal_chunks")
            received_chunks = len([name for name in os.listdir(chunks_path) if
                                   os.path.isfile(os.path.join(chunks_path, name)) and name.endswith(".tmp")])

            return received_chunks == total_chunks

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def reassemble_file(cls, user_id, project_id, file_name):
        try:
            chunks_path = os.path.join(cls.BASE_UPLOAD_FOLDER, f"user_{user_id}",
                                       f"project_{project_id}", "temporal_chunks")

            if not os.path.exists(chunks_path):
                Logger.add_to_log("error", f"El directorio de chunks no existe: {chunks_path}")
                return None

            file_extension = file_name.split(".")[-1]
            final_file_name = f"memoryFile_{project_id}.{file_extension}"
            final_file_path = os.path.join(cls.BASE_UPLOAD_FOLDER, f"user_{user_id}",
                                           f"project_{project_id}", f"memory_file")
            os.makedirs(final_file_path, exist_ok=True)

            save_path = os.path.join(final_file_path, final_file_name)

            # Asegurarse de que los trozos se procesen en el orden correcto
            chunk_files = sorted(os.listdir(chunks_path),
                                 key=lambda x: int(x.split('_')[3].split('.')[0]))

            with open(save_path, 'wb') as final_file:
                for chunk_file_name in chunk_files:
                    chunk_file_path = os.path.join(chunks_path, chunk_file_name)
                    with open(chunk_file_path, 'rb') as chunk_file:
                        final_file.write(chunk_file.read())

            # Eliminar los archivos temporales de trozos
            for chunk_file_name in chunk_files:
                os.remove(os.path.join(chunks_path, chunk_file_name))

            return save_path

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def save_and_check_image_file(cls, memory_file, user_id, project_name):
        try:
            # Asegúrate de que el archivo es válido y no vacío
            if not memory_file or memory_file.filename == '':
                return None

            upload_folder = os.path.join(cls.BASE_UPLOAD_FOLDER, "user_" + str(user_id),
                                         "project_" + str(project_name), "memory_file")
            os.makedirs(upload_folder, exist_ok=True)

            filename = secure_filename(memory_file.filename)
            save_path = os.path.join(upload_folder, filename)
            memory_file.save(save_path)

            # Aquí puedes agregar más validaciones si es necesario
            is_correct = cls.validate_file(save_path)  # Suponiendo que tienes una función de validación
            if not is_correct:
                os.remove(save_path)  # Elimina el archivo si no es válido
                return None

            return save_path  # Devuelve la ruta relativa si el archivo es válido

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def validate_file(cls, filename):
        try:
            # Implementa tu lógica de validación aquí, como comprobar tamaño, tipo, etc.
            return True

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def calculate_hashes(cls, filepath):
        # Lee el archivo en modo binario
        with open(filepath, 'rb') as f:
            contenido = f.read()

        # Calcula SHA256
        sha256 = hashlib.sha256(contenido).hexdigest()

        # Calcula SHA1
        sha1 = hashlib.sha1(contenido).hexdigest()

        # Calcula MD5
        md5 = hashlib.md5(contenido).hexdigest()

        return sha256, sha1, md5
