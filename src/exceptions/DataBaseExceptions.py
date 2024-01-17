class DataBaseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DBConnectionException(DataBaseException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DBOperationException(DataBaseException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DBProcedureException(DataBaseException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidQueryException(DataBaseException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)