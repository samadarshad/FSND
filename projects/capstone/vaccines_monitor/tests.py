from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from models import Test
from auth import requires_auth
from util import *

test_api = Blueprint('test_api', __name__)


@test_api.route('', methods=['GET'])
@requires_auth('read:all_tests')
def getTests(jwt):
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', 10, type=int)
    tests = Test.query.order_by(Test.id).paginate(
        page, items_per_page, error_out=False)
    current_tests = [t.format() for t in tests.items]
    total_number = len(Test.query.all())

    return jsonify({'tests': current_tests, 'total_number': total_number})


@test_api.route('/<id>', methods=['GET'])
@requires_auth('read:all_tests')
def getTest(jwt, id):
    test = Test.query.get(id)
    if not test:
        abort(404)

    return jsonify(test.format())
