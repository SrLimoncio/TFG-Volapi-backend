from src.utils.exceptions.CustomExceptions import SecurityCustomException


class GeneralTokenError(SecurityCustomException):
    """Excepción para manejar tokens de accesp inválidos."""
    def __init__(self, message="General access token error"):
        super().__init__(message)


class GeneratingTokenError(SecurityCustomException):
    """Excepción para manejar errores al generar tokens."""
    def __init__(self, message="Failed to generate access token"):
        super().__init__(message)


class InvalidTokenError(SecurityCustomException):
    """Excepción para manejar tokens de accesp inválidos."""
    def __init__(self, message="Access token is invalid"):
        super().__init__(message)


class TokenExpiredError(SecurityCustomException):
    """Excepción para manejar tokens de accesp expirados."""
    def __init__(self, message="Access token has expired"):
        super().__init__(message)
