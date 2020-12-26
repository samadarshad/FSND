from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from models import Patient
from auth import requires_auth
import patient_user_management
import os
import config
from util import *

patient_api = Blueprint('patient_api', __name__)


@patient_api.route('', methods=['POST'])
@requires_auth('create:patient')
def createPatient(jwt):
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
        print("Note: patient email may already exist in auth0 database")
        abort(500)        
    return jsonify({
        'success': True,
        'email': email,
        'password': password,
        'patientId': new_patient.id
    })

# @requires_auth('delete:patient')
@patient_api.route('/<id>', methods=['DELETE'])
def deletePatient(id):
    patient = Patient.query.get(id)
    if not patient:
        abort(404)
    try:
        patient_user_management.deletePatientUser(patient.user_id)
        patient.delete()
        return jsonify({
        'success': True
        })
    except Exception:
        abort(422)