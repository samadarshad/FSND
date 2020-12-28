from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from models import Patient, Test
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

    new_patient = Patient(user_id=None, name=name,
                          age=age, had_covid=had_covid)
    try:
        new_patient.insert()
        email = formEmail(new_patient.id)
        password = formPassword()
        user_id = patient_user_management.createPatientUser(email, password)
        new_patient.user_id = user_id
        new_patient.update()
    except Exception:
        print("Note: patient email may already exist in auth0 database")
        abort(500)
    return jsonify({
        'success': True,
        'email': email,
        'password': password,
        'patientId': new_patient.id
    })


@patient_api.route('/<id>', methods=['DELETE'])
@requires_auth('delete:patient')
def deletePatient(jwt, id):
    patient = getInstanceOrAbort(Patient, id)
    try:
        patient_user_management.deletePatientUser(patient.user_id)
        patient.delete()
        return jsonify({
            'success': True
        })
    except Exception:
        abort(422)


@patient_api.route('/<id>', methods=['GET'])
@requires_auth('read:patient')
def getPatient(jwt, id):
    patient = getInstanceOrAbort(Patient, id)

    if 'read:all_patients' in jwt['permissions'] or patient.user_id == jwt['sub']:
        pass
    else:
        abort(403)

    return jsonify(patient.format())


@patient_api.route('', methods=['GET'])
@requires_auth('read:all_patients')
def getAllPatient(jwt):
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', 10, type=int)
    patients = Patient.query.order_by(Patient.id).paginate(
        page, items_per_page, error_out=False)
    current_patients = [p.format() for p in patients.items]
    total_number_of_patients = len(Patient.query.all())

    return jsonify({'patients': current_patients, 'total_number_of_patients': total_number_of_patients})


@patient_api.route('/<id>', methods=['PATCH'])
@requires_auth('patch:patient')
def patchPatient(jwt, id):
    patient = getInstanceOrAbort(Patient, id)

    if 'patch:all_patients' in jwt['permissions'] or patient.user_id == jwt['sub']:
        pass
    else:
        abort(403)

    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    had_covid = body.get('had_covid', None)

    if name:
        patient.name = name
    if age:
        patient.age = age
    if had_covid:
        patient.had_covid = had_covid

    try:
        patient.update()
    except Exception:
        abort(400)

    return jsonify(patient.format())


@patient_api.route('/<id>', methods=['POST'])
@requires_auth('post:patient')
def postPatient(jwt, id):
    getInstanceOrAbort(Patient, id)

    body = request.get_json()
    effective = body.get('effective', None)
    vaccine_id = body.get('vaccine_id', None)

    if not vaccine_id:
        abort(400)

    new_test = Test(effective=effective, patient_id=id, vaccine_id=vaccine_id)
    try:
        new_test.insert()
    except Exception:
        abort(500)
    return jsonify(new_test.formatShort())
