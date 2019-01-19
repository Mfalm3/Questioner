"""Base test file"""
import unittest
from app import create_app
from app.db import init_dbase, tables_tear_down


class BaseTest(unittest.TestCase):
    """Base test class"""

    def setUp(self):
        """Test set up configs. Run before each test"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.mime_type = "application/json"
        self.signup_url = "api/v2/auth/signup"
        self.signup_payload0 = {
            "firstname": "J",
            "lastname": "Waithaka",
            "password": "password",
            "othername": "JW",
            "email": "test@gmail.com",
            "phoneNumber": "254722222222",
            "username": "waithaka",
            "registered": "now",
            "isAdmin": "True"
        }
        with self.app.app_context():
            self.db = init_dbase('testing')

    def tearDown(self):
        with self.app.app_context():
            self.db = tables_tear_down()
        self.client = None
