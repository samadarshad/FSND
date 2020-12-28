from flask import Blueprint, jsonify
from auth import AuthError

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@blueprint.app_errorhandler(400)
def bad_request(error):
    return jsonify({
        "description": "Bad request"
    }), 400


@blueprint.app_errorhandler(401)
def unauthorized(error):
    return jsonify({
        "description": "Unauthorized"
    }), 401


@blueprint.app_errorhandler(403)
def forbidden(error):
    return jsonify({
        "description": "Forbidden"
    }), 403


@blueprint.app_errorhandler(404)
def not_found(error):
    return jsonify({
        "description": "Resource not found"
    }), 404


@blueprint.app_errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "description": "Method not allowed"
    }), 405


@blueprint.app_errorhandler(422)
def unprocessible_entity(error):
    return jsonify({
        "description": "Unprocessible entity"
    }), 422


@blueprint.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "description": "Internal server error"
    }), 500
