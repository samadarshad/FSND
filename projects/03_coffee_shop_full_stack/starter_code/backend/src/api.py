import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
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
    return "hello"

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
## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
@cross_origin()
def get_drinks():
    drinks = Drink.query.all()
    drinks = [d.short() for d in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
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


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@cross_origin()
@requires_auth('post:drinks')
def post_drinks(jwt):
    body = request.get_json()
    recipe = body.get('recipe', None)
    title = body.get('title', None)
    print(recipe)
    print(title)

    #TODO get request properly and insert into db
    drinks = Drink.query.all()
    drinks = [d.long() for d in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['PATCH'])
@cross_origin()
@requires_auth('patch:drinks')
def patch_drinks(jwt, id):
    body = request.get_json()
    recipe = body.get('recipe', None)
    title = body.get('title', None)
    print(recipe)
    print(title)
    drink = Drink.query.get(id)
    if title:
        drink.title = title
    if recipe:
        drink.recipe = recipe

    drink.update()
    #TODO get request properly and insert into db
    # drink = Drink.query.get(id).long()
    # drinks = [d.long() for d in drinks]
    return jsonify({
        'success': True,
        'drinks': [Drink.query.get(id).long()]
    }), 200

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['DELETE'])
@cross_origin()
@requires_auth('delete:drinks')
def delete_drinks(id, jwt):  
    #TODO delete properly
    return jsonify({
        'success': True,
        'delete': id
    }), 200

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
