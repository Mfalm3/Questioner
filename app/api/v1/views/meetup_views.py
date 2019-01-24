# Meetups Views.
from flask import Blueprint, request, jsonify
from ..models.meetups_model import MeetupsModel
from ..utils.utils import requires_token
from app.api.v1.utils.validator import is_empty, required_length, meetup_exists


v1_meetup_blueprint = Blueprint('v1_m', __name__, url_prefix='/api/v1')
the_meetup = MeetupsModel()


@v1_meetup_blueprint.route('/meetups', methods=['POST'])
@requires_token
def create_meetup(user):
    """Create a meetup route."""
    required = ['topic', 'location', 'happeningOn', 'tags']
    if not user['isAdmin'] is True:
        return jsonify({
            "status": 403,
            "error": "Action requires Admin Priviledges"
        }), 403
    try:
        data = request.get_json()
        for item in required:
            if item not in data.keys():
                return jsonify({
                    'status': 400,
                    'error': "Please provide the following fields. "\
                    "`{}`".format(item)
                })
        for key, value in data.items():
            if isinstance(value, str):
                if is_empty(value):
                    return jsonify({
                        "status": 400,
                        "message": "{} is missing.".format(key)
                    }), 400
                if isinstance(value, list):
                    values_list = ','.join(item for item in value)
                    values_list = values_list.split(',')
                else:
                    value = value.split(',')

        topic = data.get('topic')
        location = data.get('location')
        images = data.get('images')
        happening_on = data.get('happeningOn')
        tags = data.get('tags')

        topic_length = required_length(topic, "topic", 10)
        if topic_length is not True:
            return jsonify({
                "status": 400,
                "error": topic_length
            }), 400
        location_length = required_length(location, "location", 10)
        if location_length is not True:
            return jsonify({
                "status": 400,
                "error": location_length
            }), 400

        if meetup_exists(topic, meetup_db=the_meetup.db):
            return jsonify({
                "status": 409,
                "error": "A meetup with that topic already exists!"
            }), 409
        new_meetup = the_meetup.meetup(location=location,
                                       images=images, topic=topic,
                                       happeningOn=happening_on, tags=tags)
        the_meetup.create(new_meetup)
        return jsonify({
            "status": 201,
            "message": "Meetup created successfully!",
            "data": [{
                "topic": topic,
                "location": location,
                "happeningOn": happening_on,
                "tags": tags
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
    required_key = ["response"]
    try:
        data = request.get_json()
        resp = data.get('response')
        for fields in required_key:
            for key, value in data.items():
                if fields not in data.keys():
                    return jsonify({
                        "status": 400,
                        "error": "Please provide the following " \
                        "fields. `{}`".format(key)
                    }), 400
                if value not in required:
                    return jsonify({
                        "status": 400,
                        "error": "Only the following responses are allowed. " \
                        "{}".format([item for item in required])
                        }), 400
                new_rsvp = the_meetup.rsvp(meetup=meetup, user=user, response=resp)
                return the_meetup.create_rsvp(rsvp=new_rsvp)

    except Exception as e:
        if str(e) == "list index out of range":
            return jsonify({
                "status": 400,
                "error": "The meetup with the given id is not found"
                }), 400
