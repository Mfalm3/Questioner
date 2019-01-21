"""Base test class"""
import unittest
from app import create_app
from app.db import tables_tear_down


class BaseTest(unittest.TestCase):
    """Initialize the Base test"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.signup_url = 'api/v2/auth/signup'
        self.mime_type = "application/json"
        self.signup_payload0 = {
            "firstname": "J",
            "lastname": "Waithaka",
            "password": "password",
            "othername": "JW",
            "email": "tes.t@gmail.com",
            "phoneNumber": "254722222222",
            "username": "waithaka",
            "registered": "now",
            "isAdmin": "True"
        }
        self.signup_payload1 = {
            "firstname": "Jose",
            "lastname": "Waithaka",
            "password": "password",
            "othername": "JW",
            "email": "joseph@gmail.com",
            "phoneNumber": "254722222222",
            "username": "Joseph",
            "registered": "now",
            "isAdmin": "False"
        }

    def tearDown(self):
        self.client = None
        self.db = tables_tear_down()
