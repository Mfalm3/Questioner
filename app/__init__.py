# Initializing the app.
from flask import Flask
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

    return app
