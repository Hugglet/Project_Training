from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_jwt_extended import JWTManager
from app.controllers import (
    main_blueprint,
    event_blueprint,
    place_blueprint,
    user_blueprint,
    record_blueprint,
    review_blueprint
)
from app.exception_handlers import CustomException, handle_custom_error, handle_generic_error

app = Flask(__name__, template_folder="app/templates/") # initialize app
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
jwt = JWTManager(app)
bootstrap = Bootstrap5(app)

app.register_blueprint(main_blueprint)
app.register_blueprint(event_blueprint, url_prefix="/events")
app.register_blueprint(place_blueprint, url_prefix="/places")
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(record_blueprint, url_prefix="/records")
app.register_blueprint(review_blueprint, url_prefix="/reviews")

app.register_error_handler(CustomException, handle_custom_error)
app.register_error_handler(Exception, handle_generic_error)

if __name__ == '__main__':
    app.run(debug=True)
