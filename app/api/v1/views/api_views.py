from flask import Blueprint, request, jsonify

from app.api.v1.utils.validator import valid_email, email_exists, username_exists
from app.db import init_db
from app.api.v1.models.users_model import UsersModel


v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
user = UsersModel()
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
