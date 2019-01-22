""" Users Model Class v2"""
import datetime
from werkzeug.security import generate_password_hash
from app.api.v2.models.base_model import BaseModel
from app.db import database_transactions


class UsersModel(BaseModel):
    """Model class for users."""

    def __init__(self, fname, lname, email, password, phone_number, username,
                 is_admin, other_name=''):
        """Initialize the users model."""
        super(UsersModel, self).__init__()
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = self.hashed_pw(password)
        self.phone_number = phone_number
        self.username = username
        self.is_admin = is_admin
        self.other_name = other_name

    def hashed_pw(self, password):
        """Passsword hasher"""
        hashed = generate_password_hash(password)
        return hashed

    def save(self):
        store = """
        INSERT INTO users(firstname, lastname, othername, email,
        password, phoneNumber, username, isAdmin, registered ) VALUES (
        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
            self.fname, self.lname, self.other_name, self.email,
            self.password, self.phone_number, self.username, self.is_admin,
            datetime.datetime.now()
        )

        database_transactions(store)
        user = {
            "firstname": self.fname,
            "lastname": self.lname,
            "othername": self.other_name,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "username": self.username,
            "isAdmin": self.is_admin,
            "registered_at": datetime.datetime.now()
        }

        return user

    @staticmethod
    def get_user(email):
        try:
            sql = "SELECT * FROM users where email = '{}';".format(email)

            cur = database_transactions(sql)
            user = cur.fetchone()
            return user
        except Exception as e:
            raise e
