# project_exceptions.py
from src.utils.exceptions.exceptions import SQLExecutionError


class GenericProjectError(SQLExecutionError):
    def __init__(self, message="Error general ProjectModel"):
        super().__init__(message)


class NotValidInputsProjectError(SQLExecutionError):
    def __init__(self, message="Parámetros de entrada no válidos"):
        super().__init__(message)


class DuplicateProjectError(SQLExecutionError):
    def __init__(self, message="Ya existe un proyecto con ese nombre"):
        super().__init__(message)


class NotFoundProjectError(SQLExecutionError):
    def __init__(self, message="No se pudo acceder al proyecto"):
        super().__init__(message)

# Otras excepciones relacionadas con proyectos...
