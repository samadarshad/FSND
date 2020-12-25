import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_moment import Moment

from models import setup_db
import error_handlers
from auth import requires_auth
import config
from patients import patient_api

app = Flask(__name__)
moment = Moment(app)
app.register_blueprint(error_handlers.blueprint)
app.register_blueprint(patient_api, url_prefix='/patients')
setup_db(app)
CORS(app)


@app.route('/')
def get_greeting():
    excited = os.getenv('EXCITED')
    greeting = "Hello" 
    if excited == 'true': greeting = greeting + "!! !!!"
    return greeting

@app.route('/coolkids')
def be_cool():
    return "Be cool, man, be coooool! You're almost a FSND grad!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
