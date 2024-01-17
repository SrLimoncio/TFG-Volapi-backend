class AuthException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsException(AuthException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(AuthException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)