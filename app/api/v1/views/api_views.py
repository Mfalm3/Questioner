# App views.
from .user_views import v1_user_blueprint
from .meetup_views import v1_meetup_blueprint
from .questions_view import v1_questions_blueprint


v1_meetups = v1_meetup_blueprint
v1_questions = v1_questions_blueprint
v1_users = v1_user_blueprint
