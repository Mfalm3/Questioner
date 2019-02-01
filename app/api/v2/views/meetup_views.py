# Meetups Views v2.
import datetime
from flask import Blueprint, jsonify, request
from app.api.v2.models.meetups_model import MeetupsModel, RsvpModel
from app.api.v2.models.users_model import UsersModel
from app.api.v2.utils.validator import is_empty
from app.api.v2.utils.utils import requires_token

V2_MEETUP_BLUEPRINT = Blueprint('v2_meetup_blueprint',
                                __name__, url_prefix='/api/v2')


@V2_MEETUP_BLUEPRINT.route('/meetups', methods=["POST"])
@requires_token
def create_meetup(logged_user):
    """Create a meetup view"""
    try:
        user = UsersModel.get_user(logged_user['email'])
        if user.get('isadmin') is False:
            return jsonify({
                "status": 403,
                "error": "Action requires admin privilidges!"
            }), 403

        data = request.json
        for key in data.keys():
            if key not in ['topic', 'location', 'happeningOn', 'tags']:
                return jsonify({
                    "status": 400,
                    "error": "{} field is missing".format(key)
                }), 400
        topic = data.get('topic')
        location = data.get('location')
        happening_on = data.get('happeningOn')
        try:
            check_date = happening_on.split('T')[0]
            now = datetime.datetime.now()
            check_date = datetime.datetime.strptime(check_date,
                                                    '%Y-%m-%d %H:%M%p')
            if now > check_date:
                return jsonify({
                    "status": 400,
                    "error": "You can only post a meetup with"
                             " a date in the future!"
                })

        except ValueError:
            return jsonify({
                "status": 400,
                "error": "Incorrect date format, should be YYYY-MM-DD"
                         " and correct values passed for month and date!"
            })

        tags = data.get('tags')
        if isinstance(tags, list):
            tags = ','.join([item for item in tags])
        elif isinstance(tags, str):
            tags = tags

        for key, value in data.items():
            if is_empty(value):
                return jsonify({
                    "status": 400,
                    "error": "{} field is missing".format(key)
                }), 400

        user_id = logged_user.get('user_id')
        new_meetup = MeetupsModel(topic=topic,
                                  location=location,
                                  tags=tags,
                                  happening_on=happening_on,
                                  user_id=user_id
                                  )
        data = new_meetup.save()
        return jsonify({
            "status": 201,
            "message": "Meetup created successfully!",
            "data": data
        }), 201

    except Exception as e:
        return jsonify({
            "status": 400,
            "error": str(e)
        }), 400


@V2_MEETUP_BLUEPRINT.route('/meetups/upcoming', methods=['GET'])
def get_upcoming_meetup():
    """Get all upcoming meetup records."""
    try:
        data = MeetupsModel.get_upcoming()
        return jsonify({
            "status": 200,
            "data": data
        }), 200

    except Exception as e:
        raise e


@V2_MEETUP_BLUEPRINT.route('/meetups/<meetup_id>', methods=['DELETE'])
@requires_token
def delete_meetup(logged_user, meetup_id):
    """Delete a meetup view"""
    end_id = request.path.split('/')[-1]
    if not end_id.isdigit():
        return jsonify({
            "status": 400,
            "error": "The url requires only digits for the id!"
        }), 400
    try:
        user = UsersModel.get_user(logged_user['email'])
        if user.get('isadmin') is False:
            return jsonify({
                "status": 403,
                "error": "Action requires admin privilidges!"
            }), 403

        MeetupsModel.delete(meetup_id)
        return jsonify({
            "status": 200,
            "message": "Meetup deleted successfully!"
        })

    except Exception as e:
        return jsonify({
            "status": 400,
            "error": str(e)
        })


@V2_MEETUP_BLUEPRINT.route('/meetups/<meetup_id>', methods=['GET'])
def get_specific_meetup(meetup_id):
    """Get a specific meetup record"""
    end_id = request.path.split('/')[-1]
    if not end_id.isdigit():
        return jsonify({
            "status": 400,
            "error": "The url requires only digits for the id!"
        }), 400
    meetup = MeetupsModel.get_meetup(meetup_id)
    if meetup is not False:
        return jsonify({
            "status": 200,
            "data": meetup
            })
    return jsonify({
            "status": 404,
            "error": "The meetup with the passed id doesn't exist"
        }), 404


@V2_MEETUP_BLUEPRINT.route('/meetups/<meetup_id>/rsvps', methods=['POST'])
@requires_token
def rsvp_meetup(logged_user, meetup_id):
    """Rsvp for a meetup route"""

    meetup = meetup_id
    user = UsersModel.get_user(logged_user['email']).get('user_id')
    try:
        data = request.json
        for key, value in data.items():
            if "response" not in data.keys():
                return jsonify({
                    "status": 400,
                    "error": "{} is missing.".format(key)
                }), 400
            if value.lower() not in ['yes', 'no', 'maybe']:
                return jsonify({
                    "status": 400,
                    "error": "Only `yes`,`no`,`maybe` allowed as responses!"
                }), 400
        response = data.get('response')
        get_meetup = MeetupsModel.get_meetup(meetup)
        if get_meetup is False:
            return jsonify({
                "status": 404,
                "error": "The meetup with the passed id doesn't exist"
            }), 404
        meetup_rsvp = RsvpModel(user=user,
                                meetup=meetup,
                                status=response)
        meetup_rsvp.save()
        rsvp = {
            "meetup": meetup,
            "topic": get_meetup['meetup']['meetup_topic'],
            "status": response
        }
        return jsonify({
            "status": 201,
            "data": [rsvp]
        }), 201

    except Exception as e:
        return jsonify({
            "status": 400,
            "error": str(e)
        }), 400
