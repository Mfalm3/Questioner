"""Decorator function for generating and checking for tokens."""
from functools import wraps
import datetime
import jwt
from flask import request, jsonify
from instance.config import key
from app.api.v2.models.users_model import UsersModel


def requires_token(route):
    """Decorator for protecting endpoints"""
    @wraps(route)
    def wrapper(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({
                "status": 401,
                "error": "token is missing"
            }), 401

        try:
            logged_user = UsersModel.decode_token(token=token)
            if logged_user is False:
                return jsonify({
                    "status": 400,
                    "error": "Cannot Process the request at the moment. "
                             "Please sign in to continue!"
                }), 400
        except Exception as e:
            return jsonify({
                "status": 401,
                "error": "The token is invalid! " + str(e)
            }), 401
        return route(logged_user, *args, **kwargs)
    return wrapper


def datetime_serializer(my_value):
    if isinstance(my_value, datetime.datetime):
        return my_value.isoformat()
    raise TypeError("Unknown type")
