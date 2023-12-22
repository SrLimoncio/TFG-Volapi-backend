
class SQLExecutionError(Exception):
    def __init__(self, message="Error SQL"):
        self.message = message
        super().__init__(self.message)
