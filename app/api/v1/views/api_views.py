from flask import Blueprint, request, jsonify

from app.api.v1.utils.validator import valid_email, email_exists, username_exists
from app.db import init_db
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.meetups_model import MeetupsModel
from app.api.v1.models.questions_model import QuestionModel

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
user = UsersModel()
m = MeetupsModel()
q = QuestionModel()
user_db = init_db()


@v1.route('/signup', methods=['POST'])
def signup():
    """Sign up route."""
    data = request.json

    fname = data['firstname']
    lname = data["lastname"]
    password = data["password"]
    other_name = data["othername"] or ''
    email = data["email"]
    phone = data["phoneNumber"]
    username = data["username"]
    isAdmin = data["isAdmin"]

    if not all([data.get('firstname')]):
        return jsonify({"status": 400, "error": "{} is missing.".format("username")}), 400
    if not all([data.get('lastname')]):
        return jsonify({"status": 400, "error": "{} is missing.".format("lastname")})
    if not all([data.get('password')]):
        return jsonify({"status": 400, "error": "{} is missing.".format("password")})
    if not all([data.get('email')]):
        return jsonify({"status": 400, "error": "{} is missing.".format("email")})
    if not all([data.get('phoneNumber')]):
        return jsonify({"status": 400, "error": "{} is missing.".format("email")})
    if not all([data.get('username')]):
        return jsonify({"status": 400, "error": "{} is missing.".format("phoneNumber")})
    if not all([data.get('isAdmin')]):
        return jsonify({"status": 400, "error": "{} is missing.".format("isAdmin")})

    new_user = user.user_obj(fname=fname, lname=lname, password=password, othername=other_name, email=email, phone_number=phone, username=username, isAdmin=isAdmin)
    return user.save(new_user)


@v1.route('/meetups/upcoming', methods=['GET'])
def get_meetups():
    """Get all meetups route."""
    meetups = m.get_all()
    return jsonify({
        "status": 200,
        "data": meetups
    })


@v1.route('/meetups', methods=['POST'])
def post_question():
    """Post a question route."""
    data = request.json
    required = ["title", "meetup", "body", "createdBy"]
    if data is None:
        return jsonify({"status": 400, "error": "Please provide the required fields. {}".format([field for field in required])})
    for key, value in data.items():
        if value is None or value == "":
            return jsonify({
                "status": 400,
                "error": "{} is missing.".format(key)
            })
        else:
            title = data.get("title")
            meetup = data.get("meetup")
            body = data.get("body")
            createdBy = data.get("createdBy")

            query = q.question(title=title, body=body, meetup=meetup, author=createdBy, votes=0)
            return q.save(query)


@v1.route('/meetups/<int:meetup_id>', methods=['GET'])
def get_one(meetup_id):
    """Get a specific meetup."""
    meetup = meetup_id
    if not int(meetup):
        return jsonify({
            "status": 400,
            "error": "Wrong parameters supplied for the request"
        }), 400
    else:
        resp = m.get_meetup(meetup)
        return jsonify({
            "status": 200,
            "data": resp
        }), 200


@v1.route('/questions/<int:question_id>/upvote', methods=['PATCH'])
def upvote(question_id):
    """Upvote a specific question."""
    query = q.get_question(question_id)
    updated_votes = q.upvote(query)
    return jsonify({
        "status": 200,
        "message": "Question upvoted successfully!",
        "question": updated_votes
    })


@v1.route('/questions/<int:question_id>/downvote', methods=['PATCH'])
def downvote(question_id):
    """Downvote a specific question."""
    query = q.get_question(question_id)
    downvoted_votes = q.downvote(query)
    return jsonify({
        "status": 200,
        "message": "Question downvoted successfully!",
        "question": downvoted_votes
    })
