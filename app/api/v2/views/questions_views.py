# Question Views v2.
from flask import Blueprint, request, jsonify
from app.api.v2.models.questions_model import QuestionModel
from app.api.v2.models.comments_model import CommentsModel
from app.api.v2.utils.utils import requires_token
from app.api.v2.utils.validator import is_empty, check_if_exists

V2_QUESTION_BLUEPRINT = Blueprint('v2_question_blueprint',
                                  __name__, url_prefix='/api/v2')


@V2_QUESTION_BLUEPRINT.route('/questions', methods=['POST'])
@requires_token
def post_question(logged_user):
    """Post a question view"""
    try:
        data = request.json
        for key, value in data.items():
            if key not in ['meetup', 'title', 'body']:
                return jsonify({
                    "status": 400,
                    "error": "{} field is missing".format(key)
                }), 400
            if is_empty(value):
                return jsonify({
                    "status": 400,
                    "error": "{} field is empty".format(key)
                }), 400
        meetup = data.get('meetup')
        title = data.get('title')
        body = data.get('body')

        if check_if_exists('meetup_questions', 'question_title', title):
            return jsonify({
                "status": 409,
                "error": "A Question with that title had already been asked"
                         " in that meetup!"
            }), 409
        user_id = logged_user.get('user_id')
        new_question = QuestionModel(title=title,
                                     body=body,
                                     meetup=meetup,
                                     user=user_id)
        new_question_data = new_question.save()
        return jsonify({
            "status": 201,
            "message": "Question posted to meetup successfully!",
            "data": new_question_data
        }), 201
    except Exception as e:
        if str(e) == "'NoneType' object has no attribute 'keys'":
            return jsonify({
                "status": 400,
                "error": "Please provide the following fields"
                         " [title, body, meetup_id]"
            }), 400
        if "violates foreign key constraint" in str(e):
            return jsonify({
                "status": 400,
                "error": "That meetup for the meetup id passed"
                         " is currently not available"
            }), 400
        raise e


@V2_QUESTION_BLUEPRINT.route('/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    """Get a specific question record"""
    end_id = request.path.split('/')[-1]
    if not end_id.isdigit():
        return jsonify({
            "status": 400,
            "error": "The url requires only digits for the id!"
        }), 400
    try:
        data = QuestionModel.get_question(question_id)
        if data is not False:
            return jsonify({
                "status": 200,
                "data": data
            }), 200
        return jsonify({
            "status": 404,
            "error": "Could't find a question record with that id"
        }), 404
    except Exception as e:
        return jsonify({
            "status": 400,
            "error": str(e)
        }), 400


@V2_QUESTION_BLUEPRINT.route('/questions/<question_id>/upvote',
                             methods=['PATCH'])
@requires_token
def upvote_question(logged_user, question_id):
    """Upvote a question view"""
    end_id = request.path.split('/')[-2]
    if not end_id.isdigit():
        return jsonify({
            "status": 400,
            "error": "The url requires only digits for the id!"
        }), 400
    try:
        data = QuestionModel.get_question(question_id)
        if not data:
            return jsonify({
                "status": 404,
                "error": "The question of the id passed in does not exist"
                }), 404
        user_id = logged_user.get('user_id')
        has_voted = QuestionModel.check_has_voted(user_id, question_id,
                                                  "upvote")
        if has_voted:
            return jsonify({
                "status": 401,
                "error": "You can only vote once!"
                }), 401

        QuestionModel.vote("upvote", user_id, question_id)
        return jsonify({
            "status": 200,
            "message": "Question upvoted successfully!"
        }), 200

    except Exception as e:
        raise e


@V2_QUESTION_BLUEPRINT.route('/questions/<question_id>/downvote',
                             methods=['PATCH'])
@requires_token
def downvote_question(logged_user, question_id):
    """Downvote a question view"""
    end_id = request.path.split('/')[-2]
    if not end_id.isdigit():
        return jsonify({
            "status": 400,
            "error": "The url requires only digits for the id!"
        }), 400
    try:
        data = QuestionModel.get_question(question_id)
        if not data:
            return jsonify({
                "status": 404,
                "error": "The question of the id passed in does not exist"
                }), 404
        user_id = logged_user.get('user_id')
        has_voted = QuestionModel.check_has_voted(user_id, question_id,
                                                  "downvote")
        if has_voted:
            return jsonify({
                "status": 401,
                "error": "You can only vote once!"
                }), 401

        QuestionModel.vote("downvote", user_id, question_id)
        return jsonify({
            "status": 200,
            "message": "Question downvoted successfully!"
        }), 200

    except Exception as e:
        raise e


@V2_QUESTION_BLUEPRINT.route('/comments', methods=['POST'])
@requires_token
def create_comment(logged_user):
    try:
        data = request.json
        for key, value in data.items():
            if key not in ['title', 'body', 'comment', 'question']:
                return jsonify({
                    "status": 400,
                    "error": "{} field is missing".format(key)
                }), 400
            if is_empty(value):
                return jsonify({
                    "status": 400,
                    "error": "{} field is empty".format(key)
                }), 400
        question_id = data.get('question')
        title = data.get('title')
        body = data.get('body')
        comment = data.get('comment')
        user_id = logged_user.get('user_id')

        if not check_if_exists('meetup_questions', 'question_id', question_id):
            return jsonify({
                "status": 404,
                "error": "Could not get the question for the id passed in"
                         " in that meetup!"
            }), 404
        new_comment = CommentsModel(question=question_id,
                                    title=title,
                                    body=body,
                                    comment=comment,
                                    user=user_id)
        response = new_comment.save()
        return jsonify({
            "status": 201,
            "message": "Comment added successfully",
            "data": [response]
        })
    except Exception as e:
        raise e
