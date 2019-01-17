# Meetups Views v2.
from flask import Blueprint

V2_MEETUP_BLUEPRINT = Blueprint('v2_meetup_blueprint',
                                __name__, url_prefix='/api/v2')
