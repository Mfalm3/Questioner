# User Views v2.
from flask import Blueprint, request, jsonify
from app.api.v2.utils.validator import valid_email, check_if_exists
from app.api.v2.models.users_model import UsersModel

V2_USER_BLUEPRINT = Blueprint('v2_user_blueprint',
                              __name__, url_prefix='/api/v2')


@V2_USER_BLUEPRINT.route('/auth/signup', methods=['POST'])
def signup():
    """Signup route"""
    required = [
        "firstname",
        "lastname",
        "password",
        "email",
        "phoneNumber",
        "username",
        "isAdmin"
    ]
    try:
        data = request.get_json()
        for field in required:
            if field not in data.keys():
                return jsonify({
                    "status": 400,
                    "error": "Please provide the following fields. "
                    "`{}`".format(field)
                })
        for key, value in data.items():
            if key in [field for field in required]:
                if not value.replace(" ", "").strip():
                    return jsonify({
                        "status": 400,
                        "error": "{} is missing.".format(key)
                    })

        first_name = data.get('firstname')
        last_name = data.get("lastname")
        password = data.get("password")
        other_name = data.get("othername") or ''
        email = data.get("email")
        phone = data.get("phoneNumber")
        username = data.get("username")
        is_admin = data.get("isAdmin")

        if not valid_email(email):
            return jsonify({
                "status": 400,
                "error": "The email provided is not in the right format"
            }), 400

        if check_if_exists('users', 'username', username):
            return jsonify({
                'status': 409,
                'error': 'That username already exists!'
            }), 409
        if check_if_exists('users', 'email', email):
            return jsonify({
                "status": 409,
                "error": "That email already exists."
                "Perhaps you want to login?"
            }), 409
        new_user = UsersModel(
            fname=first_name,
            lname=last_name,
            password=password,
            other_name=other_name,
            email=email,
            phone_number=phone,
            username=username,
            is_admin=is_admin)
        data = new_user.save()
        return jsonify({
            "status": 201,
            "message": "User `{}` created "
            "successfully!".format(data['username']),
            "data": [data]
        }), 201

    except Exception as e:
        return jsonify({
            "status": 400,
            "error": str(e)
        }), 400
