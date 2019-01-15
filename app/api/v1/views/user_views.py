# User views.
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import datetime
import jwt
from app.api.v1.utils.validator import valid_email, email_exists
from app.db import init_db, user_db
from app.api.v1.models.users_model import UsersModel
from instance.config import key as enc_key
from app.api.v1.utils.validator import is_empty


v1_user_blueprint = Blueprint('v1_u', __name__, url_prefix='/api/v1')
user = UsersModel()
user_db = init_db(user_db)


@v1_user_blueprint.route('/signup', methods=['POST'])
def signup():
    """Sign up route."""
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
        if data is None:
            return jsonify({
                "status": 400,
                "error": "Please provide the required fields. {}".format([field for field in required])
            })
    except Exception:
        return jsonify({
            "status": 400,
            "error": "Please provide the required fields. {}".format([field for field in required])
        })
    fname = data.get('firstname')
    lname = data.get("lastname")
    password = data.get("password")
    other_name = data.get("othername") or ''
    email = data.get("email")
    phone = data.get("phoneNumber")
    username = data.get("username")
    isAdmin = data.get("isAdmin")

    if not fname:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format("firstname")
            }), 400
    if not lname:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format("lastname")
        }), 400
    if not password:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format("password")
        }), 400
    if not email:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format("email")
            }), 400
    if not phone:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format("phoneNumber")
            }), 400
    if not username:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format("username")
        }), 400
    if not isAdmin:
        return jsonify({
            "status": 400,
            "error": "{} is missing.".format("isAdmin")
            }), 400

    new_user = user.user_obj(
        fname=fname,
        lname=lname,
        password=password,
        othername=other_name,
        email=email,
        phone_number=phone,
        username=username,
        isAdmin=isAdmin)
    return user.save(new_user)


@v1_user_blueprint.route('/login', methods=['POST'])
def login():
    """Log in route."""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if is_empty(email):
        return jsonify({
            "status": 400,
            "error": "email is missing."
        })
    if is_empty(password):
        return jsonify({
            "status": 400,
            "error": "password is missing."
        })

    if valid_email(email):
        if email_exists(email, user_db):
            cur_user = user.get_user(email)
            if cur_user and \
                    check_password_hash(
                            cur_user.get('password'), password):
                data = {
                    "email": email,
                    "sub": email,
                    "exp": datetime.datetime.now()
                           + datetime.timedelta(minutes=5)
                }
                token = jwt.encode(data, enc_key, algorithm='HS256')

                if token:
                    return jsonify({
                        "status": 200,
                        "message": "Logged in successfully!",
                        "token": token.decode('utf-8')
                        })
                else:
                    return jsonify({
                        "status": 401,
                        "error": "Could not verify token. \
                        Please sign in again!",
                        "token": token.decode('utf-8')
                        })

        else:
            return jsonify({
                "status": 400,
                "error": "No user found with the given credentials"
                }), 400
    else:
        return jsonify({
            "status": 400,
            "error": "Email invalid"
        })
