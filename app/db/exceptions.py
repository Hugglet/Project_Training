class DBException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NotFoundModelException(DBException):
    def __init__(self, message: str = "Не найдена модель"):
        super().__init__(message)