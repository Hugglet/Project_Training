

from flask import Flask

app = Flask(__name__) # initialize app
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

if __name__ == '__main__':
    app.run(debug=True)