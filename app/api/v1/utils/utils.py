import jwt
from flask import request, jsonify
from instance.config import key
from app.api.v1.models.users_model import UsersModel

u = UsersModel()


def requires_token(route):
    def wrapper(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({
                "status": 401,
                "error": "missing token"
                }), 401

        try:
            data = jwt.decode(token, key, algorithms='HS256')
            user = u.get_user(data['email'])
            if user is False:
                return jsonify({
                    "status": 404,
                    "error": "User with given credentials was not found on the system"
                    })
        except Exception as e:
            return jsonify({
                "status": 401,
                "error": "The token is invalid! "+ str(e),
            }), 401

        return route(user, *args, **kwargs)
    return wrapper
