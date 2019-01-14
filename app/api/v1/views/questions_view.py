"""Questions Views."""
from flask import Blueprint, request, jsonify
from ..models.questions_model import QuestionModel


v1_questions_blueprint = Blueprint('v1_q', __name__, url_prefix='/api/v1')
q = QuestionModel()


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
        new_question = q.question(title=title, body=body,
                                  meetup=meetup, author=createdBy, votes=0)
        return q.save(new_question)


@v1_questions_blueprint.route('/questions/<int:question_id>/upvote', methods=['PATCH'])
def upvote(question_id):
    """Upvote a specific question."""
    query = q.get_question(question_id)
    updated_votes = q.upvote(query)
    return jsonify({
        "status": 200,
        "message": "Question upvoted successfully!",
        "question": updated_votes
    })


@v1_questions_blueprint.route('/questions/<int:question_id>/downvote', methods=['PATCH'])
def downvote(question_id):
    """Downvote a specific question."""
    query = q.get_question(question_id)
    downvoted_votes = q.downvote(query)
    return jsonify({
        "status": 200,
        "message": "Question downvoted successfully!",
        "question": downvoted_votes
    })
