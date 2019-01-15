# Initializing the app.
from flask import Flask, jsonify
from app.api.v1.views.api_views import v1_users, v1_meetups, v1_questions
from instance.config import app_config


def create_app(config='development'):
    """Initialize the app function."""
    app = Flask(__name__)
    app.register_blueprint(v1_users, url_prefix='/api/v1')
    app.register_blueprint(v1_meetups, url_prefix='/api/v1')
    app.register_blueprint(v1_questions, url_prefix='/api/v1')
    app.config.from_object(app_config[config])
    app.config.from_pyfile('../instance/config.py')

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Error handler for method not allowed"""
        return jsonify({
            'error': 'Method not allowed',
            'status': 405
            }), 405

    @app.errorhandler(404)
    def url_not_found(error):
        """Error handler for url not found"""
        return jsonify({
            'error': 'The requested URL was not found on the server',
            'status': 404
            }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Error handler for url not found"""
        return jsonify({
            'error': 'Internal server error',
            'status': 500
            }), 500

    return app
