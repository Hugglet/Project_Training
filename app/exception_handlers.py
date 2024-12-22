from flask import jsonify
from main import app


class CustomException(Exception):
    """Пользовательское исключение для обработки ошибок."""
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

@app.errorhandler(CustomException)
def handle_custom_error(error: CustomException):
    response = {"error": error.message}
    return jsonify(response), error.status_code