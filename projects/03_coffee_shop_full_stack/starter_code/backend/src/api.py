import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin
from . import error_handlers
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
app.register_blueprint(error_handlers.blueprint)
setup_db(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


@app.route('/')
def index():
    return "visit /test_drop to clear the database, and /test_add to add mock data"


@app.route('/test_drop')
def test_drop_all():
    db_drop_and_create_all()
    return "reset"


@app.route('/test_add')
def test_add_drinks():
    req_title = 'drink1'
    req_recipe = [{"color": "blue", "name": "abc", "parts": 1}]
    drink = Drink(title=req_title, recipe=json.dumps(req_recipe))
    drink.insert()

    req_title = 'drink2'
    req_recipe = [{"color": "blue", "name": "abc", "parts": 1}]
    drink = Drink(title=req_title, recipe=json.dumps(req_recipe))
    drink.insert()

    req_title = 'drink3'
    req_recipe = [{"color": "green", "name": "abc", "parts": 1}]
    drink = Drink(title=req_title, recipe=json.dumps(req_recipe))
    drink.insert()
    return "added"


@app.route('/drinks')
@cross_origin()
def get_drinks():
    drinks = Drink.query.all()
    drinks = [d.short() for d in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


@app.route('/drinks-detail')
@cross_origin()
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    drinks = Drink.query.all()
    drinks = [d.long() for d in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


@app.route('/drinks', methods=['POST'])
@cross_origin()
@requires_auth('post:drinks')
def post_drinks(jwt):
    body = request.get_json()
    recipe = body.get('recipe', [])
    title = body.get('title', None)
    if not title or not recipe:
        abort(400)
    if type(recipe) != list:
        recipe = [recipe]
    drink = Drink(title=title, recipe=json.dumps(recipe))
    try:
        drink.insert()
    except Exception:
        abort(422)
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200


@app.route('/drinks/<id>', methods=['PATCH'])
@cross_origin()
@requires_auth('patch:drinks')
def patch_drinks(jwt, id):
    body = request.get_json()
    recipe = body.get('recipe', None)
    title = body.get('title', None)
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    if title:
        drink.title = title
    if recipe:
        drink.recipe = json.dumps(recipe)
    try:
        drink.update()
    except Exception:
        abort(422)
    return jsonify({
        'success': True,
        'drinks': [Drink.query.get(id).long()]
    }), 200


@app.route('/drinks/<id>', methods=['DELETE'])
@cross_origin()
@requires_auth('delete:drinks')
def delete_drinks(jwt, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        drink.delete()
    except Exception:
        abort(422)
    return jsonify({
        'success': True,
        'delete': id
    }), 200
