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
                "error": "missing token",
                'headers': request.headers
                }), 401

        try:
            data = jwt.decode(token, key, algorithm='HS256')
            user = u.get_user(data['email'])
        except Exception as e:
            return jsonify({
                "status": 401,
                "message": "The token is invalid! "+ str(e),
            }), 401

        return route(user, *args, **kwargs)
    return wrapper
