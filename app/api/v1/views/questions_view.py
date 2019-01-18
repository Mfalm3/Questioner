# Questions Views.
from flask import Blueprint, request, jsonify
from ..models.questions_model import QuestionModel


v1_questions_blueprint = Blueprint('v1_q', __name__, url_prefix='/api/v1')
QUESTION_MODEL = QuestionModel()


@v1_questions_blueprint.route('/questions', methods=['POST'])
def post_question():
    """Post a question route."""
    required = ["title", "meetup", "body", "createdBy"]
    try:
        data = request.get_json()
        for items in required:
            if items not in data.keys():
                return jsonify({
                    "status": 400,
                    "error": "Please provide the following fields. " \
                     "`{}`".format(items)
                })
            for key, value in data.items():
                if not value.replace(" ", "").strip():
                    return jsonify({
                        "status": 400,
                        "error": "{} is missing.".format(key)
                        })
        title = data.get("title")
        meetup = data.get("meetup")
        body = data.get("body")
        created_by = data.get("createdBy")
        if created_by:
            if isinstance(created_by, str):
                if not created_by.isdigit():
                    return jsonify({
                        "status": 400,
                        "error": "Can only pass digits for user id!"
                    })
            if isinstance(created_by, int):
                created_by = created_by
        if meetup:
            if isinstance(meetup, str):
                if not meetup.isdigit():
                    return jsonify({
                        "status": 400,
                        "error": "Can only pass digits for meetup id!"
                    })
            if isinstance(meetup, int):
                meetup = meetup
        new_question = QUESTION_MODEL.question(title=title,
                                               body=body,
                                               meetup=meetup,
                                               author=created_by,
                                               votes=0)
        return QUESTION_MODEL.save(new_question)
    except Exception:
        return jsonify({
            "status": 400,
            "error": "Please provide the following fields. " \
            "{}".format([items for items in required])
        })


@v1_questions_blueprint.route('/questions/<int:question_id>', methods=['GET'])
def get_meetup_question(question_id):
    """Get a pecific question"""
    question = question_id
    try:
        if not int(question):
            return jsonify({
                "status": 400,
                "error": "Wrong parameters supplied for the request"
            }), 400

        response = QUESTION_MODEL.get_question(question)
        return jsonify({
            "status": 200,
            "data": response
            }), 200

    except Exception:
        return jsonify({
            "status": 404,
            "error": "The question of the given id is not found"
                }), 404


@v1_questions_blueprint.route('/questions/<int:question_id>/upvote',
                              methods=['PATCH'])
def upvote(question_id):
    """Upvote a specific question."""
    try:
        query = QUESTION_MODEL.get_question(question_id)
        updated_votes = QUESTION_MODEL.upvote(query)
        return jsonify({
            "status": 200,
            "message": "Question upvoted successfully!",
            "question": updated_votes
        })

    except Exception:
        return jsonify({
            "status": 404,
            "error": "The question of the given id is not found"
                }), 404


@v1_questions_blueprint.route('/questions/<int:question_id>/downvote',
                              methods=['PATCH'])
def downvote(question_id):
    """Downvote a specific question."""
    try:
        query = QUESTION_MODEL.get_question(question_id)
        downvoted_votes = QUESTION_MODEL.downvote(query)
        return jsonify({
            "status": 200,
            "message": "Question downvoted successfully!",
            "question": downvoted_votes
        })

    except Exception:
        return jsonify({
            "status": 404,
            "error": "The question of the given id is not found"
                }), 404
