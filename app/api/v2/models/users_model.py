""" Users Model Class v2"""
import datetime
from werkzeug.security import generate_password_hash
from app.api.v2.models.base_model import BaseModel
from app.db import init_dbase


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
        self.db = init_dbase()

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

        conn = self.db
        cur = conn.cursor()
        cur.execute(store)
        conn.commit()
        conn.close()
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
