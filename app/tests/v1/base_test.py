""" Base Test Class"""

import unittest
import datetime
from app import create_app


class BaseTest(unittest.TestCase):
    """Define base test configurations across all tests"""

    def setUp(self):
        self.client = create_app('testing').test_client()
        self.mime_type = 'application/json'
        self.user1 = {
            "id": 1,
            "firstname": "Joe",
            "lastname": "Waithaka",
            "password": "password",
            "othername": "JW",
            "email": "test@gmail.com",
            "phoneNumber": "254722222222",
            "username": "waithaka",
            "registered": datetime.datetime.now().strftime("%I:%M%p %d %b %Y"),
            "isAdmin": "True",
        }
        self.login_payload = {
            "email": self.user1['email'],
            "password": self.user1['password']
        }
        self.meetup_payload = {
            "topic": "Bootcamp 36 retreat",
            "location": "Andela, Nairobi",
            "happeningOn": "2:00pm 6th Feb 2019",
            "tags": "django,flask"
                }
        self.meetup_payload0 = {
            "topic": "Bootcamp",
            "location": "Andela",
            "happeningOn": "2:00pm 6th Feb 2019",
            "tags": "django,flask"
                }
        self.meetup_payload1 = {
            "topic": "Bootcamp 36 retreat",
            "location": "Andela",
            "happeningOn": "2:00pm 6th Feb 2019",
            "tags": "django,flask"
                }
        self.meetup_payload2 = {
            "topic": "Bootcamp 36 retreat",
            "location": "Andela, Nairobi",
            "happeningOn": "2:00pm 6th Feb 2019",
            "tags": ["django,flask"]
                }

    def tearDown(self):
        self.client = None
        self.login_payload = None
        self.meetup_payload0 = None
        self.meetup_payload1 = None
        self.meetup_payload2 = None
