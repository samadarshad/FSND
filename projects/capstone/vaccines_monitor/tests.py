from flask import Blueprint, request, jsonify
from models import Test
from auth import requires_auth
from util import *

test_api = Blueprint('test_api', __name__)


@test_api.route('', methods=['GET'])
@requires_auth('read:all_tests')
def getTests(jwt):
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', 10, type=int)
    return jsonify(getPaginatedTable(Test, page, items_per_page))


@test_api.route('/<id>', methods=['GET'])
@requires_auth('read:all_tests')
def getTest(jwt, id):
    test = getInstanceOrAbort(Test, id)
    return jsonify(test.format())
