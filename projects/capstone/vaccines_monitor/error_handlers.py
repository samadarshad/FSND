from flask import Blueprint, jsonify
from auth import AuthError
from auth0_management_api_wrapper import Auth0Error

blueprint = Blueprint('error_handlers', __name__)

@blueprint.app_errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@blueprint.app_errorhandler(Auth0Error)
def handle_auth0_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

##TODO make the error responses consistent with each other
    
@blueprint.app_errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@blueprint.app_errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@blueprint.app_errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


@blueprint.app_errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@blueprint.app_errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405


@blueprint.app_errorhandler(422)
def unprocessible_entity(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessible entity"
    }), 422


@blueprint.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500
