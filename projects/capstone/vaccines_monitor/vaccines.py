from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from models import Vaccine
from auth import requires_auth
from util import *

vaccine_api = Blueprint('vaccine_api', __name__)

@vaccine_api.route('', methods=['POST'])
@requires_auth('create:vaccine')
def createVaccine(jwt):
    body = request.get_json()
    name = body.get('name', None)
    
    
    new_vaccine = Vaccine(name=name)
    try:
        new_vaccine.insert()
        print(new_vaccine.format())
    except Exception:
        abort(500)        
    return jsonify(new_vaccine.format())    
    

@vaccine_api.route('', methods=['GET'])
def getVaccines():
        
    #TODO get vaccines

    return jsonify({
        'success': True
        })

@vaccine_api.route('/<id>', methods=['GET'])
def getVaccine(id):
        
    #TODO get vaccines

    return jsonify({
        'success': True
        })

@vaccine_api.route('/<id>', methods=['PATCH'])
@requires_auth('patch:vaccine')
def patchVaccine(jwt, id):
        
    #TODO 

    return jsonify({
        'success': True
        })

@vaccine_api.route('/<id>', methods=['DELETE'])
@requires_auth('delete:vaccine')
def deleteVaccine(jwt, id):
        
    #TODO 

    return jsonify({
        'success': True
        })