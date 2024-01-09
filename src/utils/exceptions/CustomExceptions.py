
class SQLCustomException(Exception):
    def __init__(self, message):
        self.message = "Error SQL: " + message
        super().__init__(self.message)


class SecurityCustomException(Exception):
    def __init__(self, message):
        self.message = "Error Security: " + message
        super().__init__(self.message)
