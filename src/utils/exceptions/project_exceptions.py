# project_exceptions.py
from src.utils.exceptions.CustomExceptions import SQLCustomException


class GenericProjectCustom(SQLCustomException):
    def __init__(self, message="Error general ProjectModel"):
        super().__init__(message)


class NotValidInputsProjectCustom(SQLCustomException):
    def __init__(self, message="Parámetros de entrada no válidos"):
        super().__init__(message)


class DuplicateProjectCustom(SQLCustomException):
    def __init__(self, message="Ya existe un proyecto con ese nombre"):
        super().__init__(message)


class NotFoundProjectCustom(SQLCustomException):
    def __init__(self, message="No se pudo acceder al proyecto"):
        super().__init__(message)

# Otras excepciones relacionadas con proyectos...
