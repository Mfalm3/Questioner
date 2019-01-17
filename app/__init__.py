# Initializing the app.
from flask import Flask, jsonify
from app.api.v1.views.api_views import v1_users, v1_meetups, v1_questions
from app.api.v2.views.api_views import v2_user_bp, v2_meetup_bp, v2_question_bp
from instance.config import app_config


def method_not_allowed(error):
    """
    This function handles errors for methods not allowed on given endpoints
    """
    return jsonify({
        'error': str(error),
        'status': 405
        }), 405


def resource_not_found(error):
    """Error handler for url not found"""
    return jsonify({
        'error': str(error),
        'status': 404
        }), 404


def internal_server_error(error):
    """Error handler internal server error"""
    return jsonify({
        'error': str(error),
        'status': 500
        }), 500


def create_app(config='development'):
    """Initialize the app function."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])
    app.config.from_pyfile('../instance/config.py')
    # v1 blueprints
    app.register_blueprint(v1_users, url_prefix='/api/v1')
    app.register_blueprint(v1_meetups, url_prefix='/api/v1')
    app.register_blueprint(v1_questions, url_prefix='/api/v1')
    # v2 blueprints
    app.register_blueprint(v2_user_bp, url_prefix='/api/v2')
    app.register_blueprint(v2_meetup_bp, url_prefix='/api/v2')
    app.register_blueprint(v2_question_bp, url_prefix='/api/v2')
    # Register error handlers
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(500, internal_server_error)

    return app
