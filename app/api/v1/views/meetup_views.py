# Meetups Views.
from flask import Blueprint, request, jsonify
from ..models.meetups_model import MeetupsModel
from ..utils.utils import requires_token
from app.api.v1.utils.validator import is_empty, required_length


v1_meetup_blueprint = Blueprint('v1_m', __name__, url_prefix='/api/v1')
the_meetup = MeetupsModel()


@v1_meetup_blueprint.route('/meetups', methods=['POST'])
@requires_token
def create_meetup(user):
    """Create a meetup route."""
    if not user['isAdmin'] == "True":
        return jsonify({
            "status": 403,
            "error": "Action requires Admin Priviledges"
        }), 403
    try:
        data = request.get_json()

        topic = data.get('topic')
        location = data.get('location')
        images = data.get('images')
        happeningOn = data.get('happeningOn')
        tags = data.get('tags')

        if isinstance(tags, list):
            tag = ','.join(item for item in tags)
            tag = tag.split(',')
        else:
            tag = tags.split(',')

        if not topic or is_empty(topic):
            return jsonify({
                "status": 400,
                "message": "{} is missing.".format("topic")
            }), 400
        topic_length = required_length(topic, "topic", 10)
        if topic_length is not True:
            return jsonify({
                "status": 400,
                "error": topic_length
            }), 400
        if not location:
            return jsonify({
                "status": 400,
                "message": "{} is missing.".format("location")
            }), 400
        location_length = required_length(location, "location", 10)
        if location_length is not True:
            return jsonify({
                "status": 400,
                "error": location_length
            }), 400
        if not happeningOn:
            return jsonify({
                "status": 400,
                "message": "{} is missing.".format("happeningOn")
            }), 400
        if not tags:
            return jsonify({
                "status": 400,
                "message": "{} is missing.".format("tags")
            }), 400

        new_meetup = the_meetup.meetup(location=location,
                                       images=images, topic=topic,
                                       happeningOn=happeningOn, tags=tag)
        the_meetup.create(new_meetup)
        return jsonify({
            "status": 201,
            "message": "Meetup created successfully!",
            "data": [{
                "topic": topic,
                "location": location,
                "happeningOn": happeningOn,
                "tags": tag
                        }]
        }), 201
    except Exception as e:
        raise e


@v1_meetup_blueprint.route('/meetups/upcoming', methods=['GET'])
def get_meetups():
    """Get all meetups route."""
    meetups = the_meetup.get_all()
    return jsonify({
        "status": 200,
        "data": meetups
    })


@v1_meetup_blueprint.route('/meetups/<int:meetup_id>', methods=['GET'])
def get_one(meetup_id):
    """Get a specific meetup."""
    meetup = meetup_id
    try:
        if not int(meetup):
            return jsonify({
                "status": 400,
                "error": "Wrong parameters supplied for the request"
            }), 400

        resp = the_meetup.get_meetup(meetup)
        return jsonify({
            "status": 200,
            "data": resp
            }), 200

    except Exception:
        return jsonify({
            "status": 404,
            "error": "The meetup of the given id is not found"
                }), 404


@v1_meetup_blueprint.route('/meetups/<int:meetup_id>/rsvps', methods=['POST'])
@requires_token
def rsvp_a_meetup(user, meetup_id):
    """Rsvp to a meetup route."""
    meetup = meetup_id
    user = user['id']
    required = ["yes", "no", "maybe"]
    try:
        data = request.get_json()
        resp = data.get('response')

        for key, value in data.items():
            if key != "response":
                return jsonify({
                    "status": 400,
                    "error": "Please provide the following" \
                    "fields. {}".format('response')
                }), 400
            if value not in required:
                return jsonify({
                    "status": 400,
                    "error": "Only the following responses are allowed. " \
                     "{}".format([item for item in required])
                    }), 400
            new_rsvp = the_meetup.rsvp(meetup=meetup, user=user, response=resp)
            return the_meetup.create_rsvp(rsvp=new_rsvp)

    except Exception:
        return jsonify({
            "status": 404,
            "error": "The meetup of the given id is not found"
            }), 404
