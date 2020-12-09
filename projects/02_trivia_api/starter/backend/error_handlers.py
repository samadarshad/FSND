from flask import Blueprint, jsonify

blueprint = Blueprint('error_handlers', __name__)

@blueprint.app_errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

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