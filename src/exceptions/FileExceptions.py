
class FileCustomException(Exception):
    def __init__(self, message):
        self.message = "Error File: " + message
        super().__init__(self.message)


class DirectoryCreationError(FileCustomException):
    """Excepción para manejar errores en la creación de directorios."""
    def __init__(self, message="Failed to create directory"):
        super().__init__(message)


class FileSavingError(FileCustomException):
    """Excepción para manejar errores al guardar archivos."""
    def __init__(self, message="Failed to save file"):
        super().__init__(message)


class FileValidationError(FileCustomException):
    """Excepción para manejar errores en la validación de archivos."""
    def __init__(self, message="File validation failed"):
        super().__init__(message)


class FileReassemblyError(FileCustomException):
    """Excepción para manejar errores en la reensamblación de archivos."""
    def __init__(self, message="Failed to reassemble file"):
        super().__init__(message)


class HashCalculationError(FileCustomException):
    """Excepción para manejar errores en el cálculo de hashes."""
    def __init__(self, message="Failed to calculate file hash"):
        super().__init__(message)


class PathNotFoundException(FileCustomException):
    def __init__(self, message="The path dont exist"):
        super().__init__(message)