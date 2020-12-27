import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_moment import Moment

from models import setup_db
import error_handlers
from auth import requires_auth
import config
from patients import patient_api
from vaccines import vaccine_api
from tests import test_api

app = Flask(__name__)
moment = Moment(app)
app.register_blueprint(error_handlers.blueprint)
app.register_blueprint(patient_api, url_prefix='/patients')
app.register_blueprint(vaccine_api, url_prefix='/vaccines')
app.register_blueprint(test_api, url_prefix='/tests')
setup_db(app)
CORS(app)


@app.route('/')
def index():
    return "Service is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
