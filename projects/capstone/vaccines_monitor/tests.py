from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from models import Test
from auth import requires_auth
from util import *

test_api = Blueprint('test_api', __name__)


@test_api.route('', methods=['GET'])
@requires_auth('read:all_tests')
def getTests(jwt):
        
    #TODO

    return jsonify({
        'success': True
        })

@test_api.route('/<id>', methods=['GET'])
@requires_auth('read:all_tests')
def getTest(jwt, id):
        
    #TODO

    return jsonify({
        'success': True
        })
