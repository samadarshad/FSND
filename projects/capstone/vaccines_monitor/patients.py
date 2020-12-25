from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from models import Patient
from auth import requires_auth
import patient_user_management
import os
import config

patient_api = Blueprint('patient_api', __name__)

# @requires_auth('create:patient')
@patient_api.route('/', methods=['POST'])
def createPatient():
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    had_covid = body.get('had_covid', None)
    
    new_patient = Patient(user_id=None, name=name, age=age, had_covid=had_covid)
    try:
        new_patient.insert()
        email = formEmail(new_patient.id)
        password = formPassword()
        user_id = patient_user_management.createPatientUser(email, password)
        new_patient.user_id = user_id
        new_patient.update()
        print(new_patient.format())
    except Exception:
        abort(500)        
    return jsonify({
        'success': True,
        'email': email,
        'password': password
    })

email_prefix = os.getenv('PATIENT_EMAIL_PREFIX')
email_suffix = os.getenv('PATIENT_EMAIL_SUFFIX')
patient_password = os.getenv('PATIENT_PASSWORD')
def formEmail(id):
    return email_prefix + str(id) + email_suffix

def formPassword():
    return patient_password