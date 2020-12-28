from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from models import Vaccine
from auth import requires_auth
from util import *

vaccine_api = Blueprint('vaccine_api', __name__)


@vaccine_api.route('', methods=['POST'])
@requires_auth('create:vaccine')
def createVaccine(jwt):
    new_vaccine = Vaccine()
    new_vaccine = populateObjectFromJson(new_vaccine, request.get_json())
    try:
        new_vaccine.insert()
    except Exception:
        abort(400)
    return jsonify(new_vaccine.format())


@vaccine_api.route('', methods=['GET'])
def getVaccines():
    vaccines = Vaccine.query.order_by(Vaccine.id).all()
    vaccines_formatted = [v.format() for v in vaccines]
    return jsonify(vaccines_formatted)


@vaccine_api.route('/<id>', methods=['GET'])
def getVaccine(id):
    vaccine = getInstanceOrAbort(Vaccine, id)
    return jsonify(vaccine.format())


@vaccine_api.route('/<id>', methods=['PATCH'])
@requires_auth('patch:vaccine')
def patchVaccine(jwt, id):
    vaccine = getInstanceOrAbort(Vaccine, id)
    vaccine = populateObjectFromJson(vaccine, request.get_json())
    try:
        vaccine.update()
    except Exception:
        abort(400)
    return jsonify(vaccine.format())


@vaccine_api.route('/<id>', methods=['DELETE'])
@requires_auth('delete:vaccine')
def deleteVaccine(jwt, id):    
    deleteInstanceOrAbort(Vaccine, id)
    return jsonify(success=True)
