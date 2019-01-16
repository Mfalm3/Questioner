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
    except Exception:
        return jsonify({
            "status": 400,
            "error": "Please provide the following fields. \
             {}".format([items for items in required])
        })
    title = data.get("title")
    meetup = data.get("meetup")
    body = data.get("body")
    createdBy = data.get("createdBy")

    if not title:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format('title')
            })
    if not meetup:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format('meetup')
            })
    if not body:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format('body')
            })
    if not createdBy:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format('createdBy')
            })
    else:
        new_question = QUESTION_MODEL.question(title=title,
                                               body=body,
                                               meetup=meetup,
                                               author=createdBy,
                                               votes=0)
        return QUESTION_MODEL.save(new_question)


@v1_questions_blueprint.route('/questions/<int:id>', methods=['GET'])
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
