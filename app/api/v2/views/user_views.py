# User Views v2.
from flask import Blueprint

V2_USER_BLUEPRINT = Blueprint('v2_user_blueprint',
                              __name__, url_prefix='/api/v2')
