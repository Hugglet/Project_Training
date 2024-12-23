from flask import Flask
from flask_bootstrap import Bootstrap5
from app import controllers

app = Flask(__name__) 
bootstrap = Bootstrap5(app)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

if __name__ == '__main__':
    app.run(debug=True)
