""" Users Model Class v2"""
import datetime
import jwt
from werkzeug.security import generate_password_hash
from app.api.v2.models.base_model import BaseModel
from app.db import database_transactions
from instance.config import key as enc_key


class UsersModel(BaseModel):
    """Model class for users."""

    def __init__(self, fname, lname, email, password, phone_number, username,
                 other_name=''):
        """Initialize the users model."""
        super(UsersModel, self).__init__()
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = self.hashed_pw(password)
        self.phone_number = phone_number
        self.username = username
        self.other_name = other_name

    def hashed_pw(self, password):
        """Passsword hasher"""
        hashed = generate_password_hash(password)
        return hashed

    @staticmethod
    def change_password(user, new_password):
        """Set a new password"""
        sql = """
        UPDATE users SET password = '{}' WHERE user_id = {}
        """.format(generate_password_hash(new_password), user)
        database_transactions(sql)

    def save(self):
        """Create a new user"""
        store = """
        INSERT INTO users(firstname, lastname, othername, email,
        password, phoneNumber, username, registered ) VALUES (
        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        returning user_id""".format(
            self.fname, self.lname, self.other_name, self.email,
            self.password, self.phone_number, self.username,
            datetime.datetime.now()
        )

        id = database_transactions(store)
        user = {
            "id": id.fetchone()['user_id'],
            "firstname": self.fname,
            "lastname": self.lname,
            "othername": self.other_name,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "username": self.username,
            "registered_at": datetime.datetime.now()
        }

        return user

    @staticmethod
    def logout(token):
        """Logout a new user"""
        sql = """
        INSERT INTO blacklisted_tokens (blacklisted_token)
        VALUES ('{}')""". format(token)

        database_transactions(sql)

    @staticmethod
    def get_user(email):
        """Get a user"""
        try:
            sql = "SELECT * FROM users where email = '{}';".format(email)

            cur = database_transactions(sql)
            user = cur.fetchone()
            return user
        except Exception as e:
            raise e

    @staticmethod
    def token_blacklisted(token):
        """Check if a token is blacklisted"""
        sql = """
        SELECT blacklisted_token as token
        FROM blacklisted_tokens
        WHERE blacklisted_token = '{}'
        """.format(token)

        blacklist = database_transactions(sql)
        if blacklist.fetchone():
            return True
        return False

    @staticmethod
    def decode_token(token):
        """Method to decode authentication token"""
        if UsersModel.token_blacklisted(token):
            return False

        data = jwt.decode(token, enc_key, algorithms='HS256')
        user = UsersModel.get_user(data['email'])
        return user
