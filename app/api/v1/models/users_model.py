"""Users Model Class"""
import datetime
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .base_model import BaseModel
from app.db import init_db, user_db
from app.api.v1.utils.validator import email_exists, username_exists, valid_email


class UsersModel(BaseModel):
    """Model class for users."""

    def __init__(self):
        """Initialize the users model."""
        super(BaseModel, self).__init__()
        self.db = init_db(user_db)

    def user_obj(self, fname, lname, password, othername, email, phone_number, username, isAdmin=False):
        """User object."""

        # timestamp =
        user = {
            "id": len(self.db) + 1,
            "firstname": fname,
            "lastname":  lname,
            "password": generate_password_hash(password),
            "othername": othername or "",
            "email": email,
            "phoneNumber": phone_number,
            "username": username,
            "registered": datetime.datetime.now().strftime("%I:%M:%S%P %d %b %Y"),
            "isAdmin": isAdmin,
        }
        return user

    def save(self, user):
        """Save a new user."""
        email = user['email']
        username = user['username']
        if valid_email(user['email']):
            if email_exists(email, user_db):
                return jsonify({
                    "status": 409,
                    "error": "Email Already Exists. Perhaps you want to login?"
                })
            else:
                if username_exists(username, user_db):
                    return jsonify({"status": 409, "error": "Username Already Exists!"}), 409
                else:
                    self.db.append(user)
                    return jsonify({"status": 201, "message": "User Created Successfully!","user": self.db}), 201
        else:
            return jsonify({
                "status": 400,
                "error": "Ensure your email is in the right format! eg. test@example.com"
            }), 400
