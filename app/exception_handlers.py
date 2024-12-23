from flask import jsonify, render_template

class CustomException(Exception):
    """Пользовательское исключение для обработки ошибок."""
    def __init__(self, message, status_code, redirect_page="main.index"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.redirect_page = redirect_page

def handle_custom_error(error: CustomException):
    return render_template("error.html", error_message=error.message, redirect_page=error.redirect_page)

def handle_generic_error(error: Exception):
    return render_template("error.html", error_message=error, redirect_page="main.index"), 500