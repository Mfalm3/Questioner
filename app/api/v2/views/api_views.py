# Api v2 views
from app.api.v2.views.meetup_views import V2_MEETUP_BLUEPRINT
from app.api.v2.views.questions_views import V2_QUESTION_BLUEPRINT
from app.api.v2.views.user_views import V2_USER_BLUEPRINT

v2_meetup_bp = V2_MEETUP_BLUEPRINT
v2_user_bp = V2_USER_BLUEPRINT
v2_question_bp = V2_QUESTION_BLUEPRINT
