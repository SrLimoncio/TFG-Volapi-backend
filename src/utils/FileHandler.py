import os
import hashlib
from werkzeug.utils import secure_filename

# Excepciones
from src.exceptions.FileExceptions import (DirectoryCreationError,
                                           FileSavingError,
                                           FileValidationError,
                                           HashCalculationError,
                                           FileReassemblyError,
                                           PathNotFoundException
                                           )


class FileHandler:
    """
    Clase para manejar operaciones relacionadas con archivos en un proyecto.

    Métodos:
    - generate_path_memory_file(user_id, project_id, file_name): Genera la ruta del archivo en memoria.
    - save_chunk_temporal_path(user_id, project_id, chunk, chunk_number): Guarda un fragmento de archivo en una ruta temporal.
    - check_all_chunks_received(user_id, project_id, total_chunks): Verifica si todos los fragmentos de un archivo han sido recibidos.
    - reassemble_file(user_id, project_id, file_name): Reensambla un archivo a partir de sus fragmentos.
    - save_and_check_image_file(memory_file, user_id, project_name): Guarda y verifica un archivo de imagen.
    - validate_file(filename): Valida un archivo (por implementar).
    - calculate_hashes(filepath): Calcula diferentes hashes (SHA256, SHA1, MD5) de un archivo.
    """

    # Define la ruta base de la carpeta userfiles
    BASE_UPLOAD_FOLDER = 'UserFiles'

    @classmethod
    def generate_path_memory_file(cls, user_id, project_id, file_name):
        """
        Genera la ruta del archivo en memoria para un usuario y proyecto específicos.

        Args:
        - user_id (int): El ID del usuario.
        - project_id (int): El ID del proyecto.
        - file_name (str): Nombre del archivo a generar.

        Returns:
        - str: La ruta generada para el archivo en memoria.

        Raises:
        - DirectoryCreationError: Si hay un error al generar la ruta del archivo.
        """
        try:
            upload_folder = os.path.join(cls.BASE_UPLOAD_FOLDER, "user_" + str(user_id),
                                         "project_" + str(project_id), "memory_file", file_name)

            return upload_folder

        except Exception as ex:
            raise DirectoryCreationError(f"Error generating path for memory file: {ex}")

    @classmethod
    def save_chunk_temporal_path(cls, user_id, project_id, chunk, chunk_number):
        """
        Guarda un fragmento de archivo en una ruta temporal.

        Args:
        - user_id (int): El ID del usuario.
        - project_id (int): El ID del proyecto.
        - chunk (File): El fragmento de archivo a guardar.
        - chunk_number (int): El número de orden del fragmento.

        Returns:
        - bool: True si el fragmento se guardó correctamente.

        Raises:
        - FileSavingError: Si hay un error al guardar el fragmento de archivo.
        """
        try:
            filename = secure_filename(f"project_{project_id}_chunk_{chunk_number}.tmp")
            upload_folder = os.path.join(cls.BASE_UPLOAD_FOLDER, "user_" + str(user_id),
                                         "project_" + str(project_id), "temporal_chunks")
            os.makedirs(upload_folder, exist_ok=True)

            save_path = os.path.join(upload_folder, filename)
            chunk.save(save_path)

            return True

        except Exception as ex:
            raise FileSavingError(f"Error saving and checking chunk file: {ex}")

    @classmethod
    def check_all_chunks_received(cls, user_id, project_id, total_chunks):
        """
        Verifica si todos los fragmentos de un archivo han sido recibidos.

        Args:
        - user_id (int): El ID del usuario.
        - project_id (int): El ID del proyecto.
        - total_chunks (int): Número total de fragmentos esperados.

        Returns:
        - bool: True si todos los fragmentos han sido recibidos.

        Raises:
        - FileValidationError: Si hay un error al validar los fragmentos recibidos.
        """
        try:
            # Contar los archivos temporales de trozos que se han guardado
            chunks_path = os.path.join(cls.BASE_UPLOAD_FOLDER, f"user_{user_id}",
                                       f"project_{project_id}", "temporal_chunks")
            received_chunks = len([name for name in os.listdir(chunks_path) if
                                   os.path.isfile(os.path.join(chunks_path, name)) and name.endswith(".tmp")])

            return received_chunks == total_chunks

        except Exception as ex:
            raise FileValidationError(f"Error validating all chunk received: {ex}")

    @classmethod
    def reassemble_file(cls, user_id, project_id, file_name):
        """
        Reensambla un archivo a partir de sus fragmentos.

        Args:
        - user_id (int): El ID del usuario.
        - project_id (int): El ID del proyecto.
        - file_name (str): El nombre del archivo final.

        Returns:
        - str: La ruta del archivo reensamblado.

        Raises:
        - FileReassemblyError: Si hay un error al reensamblar el archivo.
        - PathNotFoundException: Si no se encuentra la ruta de los fragmentos.
        """
        try:
            chunks_path = os.path.join(cls.BASE_UPLOAD_FOLDER, f"user_{user_id}",
                                       f"project_{project_id}", "temporal_chunks")

            if not os.path.exists(chunks_path):
                raise PathNotFoundException(f"Chunk path dont exist")

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
            raise FileReassemblyError(f"Error reassembling file: {ex}")

    @classmethod
    def save_and_check_image_file(cls, memory_file, user_id, project_name):
        """
        Guarda y verifica un archivo de imagen.

        Args:
        - memory_file (File): El archivo de imagen a guardar.
        - user_id (int): El ID del usuario.
        - project_name (str): El nombre del proyecto.

        Returns:
        - str: La ruta del archivo guardado si es válido, None en caso contrario.

        Raises:
        - FileSavingError: Si hay un error al guardar y verificar el archivo de imagen.
        """
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
            is_correct = cls.validate_file(save_path)
            if not is_correct:
                os.remove(save_path)  # Elimina el archivo si no es válido
                return None

            return save_path  # Devuelve la ruta relativa si el archivo es válido

        except Exception as ex:
            raise FileSavingError(f"Error saving and checking image file: {ex}")

    @classmethod
    def validate_file(cls, filename):
        """
        Valida un archivo comprobando su tamaño y si es compatible con Volatility.

        Args:
        - filename (str): Ruta del archivo a validar.

        Returns:
        - bool: True si el archivo cumple con los criterios de validación, False en caso contrario.

        Raises:
        - FileValidationError: Si ocurre un error durante la validación.
        """
        try:
            # Tamaño máximo permitido en bytes (10GB)
            MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024
            # Extensiones permitidas para Volatility
            ALLOWED_EXTENSIONS = {'bin', 'dmp', 'mem', 'raw', 'crash', 'hpa'}

            # Comprobando el tamaño del archivo
            if os.path.getsize(filename) > MAX_FILE_SIZE:
                return False

            # Comprobando la extensión del archivo
            if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
                return False

            return True

        except Exception as ex:
            raise FileValidationError(f"Error validating file: {ex}")

    @classmethod
    def calculate_hashes(cls, filepath):
        """
        Calcula y devuelve varios hashes (SHA256, SHA1, MD5) de un archivo.

        Args:
        - filepath (str): La ruta del archivo del cual se calcularán los hashes.

        Returns:
        - tuple: Contiene los hashes SHA256, SHA1 y MD5 del archivo.

        Raises:
        - HashCalculationError: Si ocurre un error durante el cálculo de los hashes.
        """
        try:
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
        except Exception as ex:
            raise HashCalculationError(f"Error calculating hashes for file: {ex}")
