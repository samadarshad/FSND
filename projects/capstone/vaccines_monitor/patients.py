from flask import Blueprint, request, abort, jsonify
from models import Patient, Test
from auth import requires_auth
import patient_user_management
import os
import config
from util import *

patient_api = Blueprint('patient_api', __name__)


@patient_api.route('', methods=['GET'])
@requires_auth('read:all_patients')
def getAllPatient(jwt):
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', 10, type=int)
    return jsonify(getPaginatedTable(Patient, page, items_per_page))


@patient_api.route('', methods=['POST'])
@requires_auth('create:patient')
def createPatient(jwt):
    new_patient = Patient()
    new_patient = populateObjectFromJson(new_patient, request.get_json())
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
        'email': email,
        'password': password,
        'patientId': new_patient.id
    })


@patient_api.route('/<id>', methods=['GET'])
@requires_auth('read:patient')
def getPatient(jwt, id):
    patient = getInstanceOrAbort(Patient, id)

    if 'read:all_patients' in jwt['permissions'] or patient.user_id == jwt['sub']:
        pass
    else:
        abort(403)

    return jsonify(patient.format())


@patient_api.route('/<id>', methods=['POST'])
@requires_auth('post:patient')
def postPatient(jwt, id):
    getInstanceOrAbort(Patient, id)
    new_test = Test()
    new_test = populateObjectFromJson(new_test, request.get_json())
    new_test.patient_id = id
    try:
        new_test.insert()
    except Exception:
        abort(400)
    return jsonify(new_test.formatShort())


@patient_api.route('/<id>', methods=['PATCH'])
@requires_auth('patch:patient')
def patchPatient(jwt, id):
    patient = getInstanceOrAbort(Patient, id)

    if 'patch:all_patients' in jwt['permissions'] or patient.user_id == jwt['sub']:
        pass
    else:
        abort(403)

    patient = populateObjectFromJson(patient, request.get_json())
    try:
        patient.update()
    except Exception:
        abort(400)

    return jsonify(patient.format())


@patient_api.route('/<id>', methods=['DELETE'])
@requires_auth('delete:patient')
def deletePatient(jwt, id):
    patient = getInstanceOrAbort(Patient, id)
    try:
        patient_user_management.deletePatientUser(patient.user_id)
    except Exception:
        abort(500)
    deleteInstanceOrAbort(Patient, id)
    return jsonify(success=True)
