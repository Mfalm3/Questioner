""" Users Model Class"""
import datetime
from flask import jsonify
from werkzeug.security import generate_password_hash
from app.db import init_db, user_db
from app.api.v1.utils.validator import (email_exists, username_exists,
valid_email, is_empty, no_numbers)
from .base_model import BaseModel


class UsersModel(BaseModel):
    """Model class for users."""

    def __init__(self):
        """Initialize the users model."""
        super(UsersModel, self).__init__()
        self.db = init_db(user_db)

    def user_obj(self,
                 fname,
                 lname,
                 password,
                 othername,
                 email,
                 phone_number,
                 username,
                 isAdmin=False):
        """User object."""

        timestamp = datetime.datetime.now().strftime("%I:%M:%S%P %d %b %Y")
        user = {
            "id": len(self.db) + 1,
            "firstname": fname,
            "lastname":  lname,
            "password": generate_password_hash(password),
            "othername": othername or "",
            "email": email,
            "phoneNumber": phone_number,
            "username": username,
            "registered": timestamp,
            "isAdmin": isAdmin,
        }
        return user

    def get_user(self, email):
        """Get a user method"""
        current_user = [user for user in self.db if user['email'] == email]
        if current_user:
            return current_user[0]
        return False

    def save(self, user):
        """Save a new user."""
        email = user['email']
        username = user['username']
        fname = user['firstname']
        lname = user['lastname']

        if is_empty(username) or is_empty(fname) or is_empty(lname):
            return jsonify({
                "status": 400,
                "error": "Fill in a name. No name should not be empty!"
            }), 400
        if not no_numbers(fname) or not no_numbers(lname):
            return jsonify({
                "status": 400,
                "error": "Names should only contain alphabet characters!"
            }), 400

        if valid_email(user['email']):
            if email_exists(email, self.db):
                return jsonify({
                    "status": 409,
                    "error": "Email Already Exists. Perhaps you want to login?"
                }), 409
            else:
                if username_exists(username, self.db):
                    return jsonify({
                        "status": 409,
                        "error": "Username Already Exists!"}), 409
                else:
                    self.db.append(user)
                    data = {
                        "email": user['email'],
                        "firstname": user['firstname'],
                        "id": user['id'],
                        "isAdmin": user['isAdmin'],
                        "lastname": user['lastname'],
                        "othername": user['othername'],
                        "phoneNumber": user['phoneNumber'],
                        "registered": user['registered'],
                        "username": user['username']
                    }
                    return jsonify({
                        "status": 201,
                        "message": "User Created Successfully!",
                        "user": data
                        }), 201
        else:
            return jsonify({
                "status": 400,
                "error": "Ensure your email is in the right " \
                "format! eg. test@example.com"
            }), 400
