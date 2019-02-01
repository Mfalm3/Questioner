"""Base test class"""
import unittest
import json
from app import create_app
from app.db import tables_tear_down


class BaseTest(unittest.TestCase):
    """Initialize the Base test"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.signup_url = 'api/v2/auth/signup'
        self.signin_url = 'api/v2/auth/login'
        self.headers = {"Content-type": "application/json"}
        self.signup_payload0 = {
            "firstname": "J",
            "lastname": "Waithaka",
            "password": "pas$5sworD",
            "othername": "JW",
            "email": "tes.t@gmail.com",
            "phoneNumber": "254722222222",
            "username": "waithaka",
        }
        self.signup_payload1 = {
            "firstname": "Jose",
            "lastname": "Waithaka",
            "password": "pas$5worD",
            "othername": "JW",
            "email": "joseph@gmail.com",
            "phoneNumber": "254722222222",
            "username": "Joseph"
        }

        self.signin_payload0 = {
            "email": "admin@email.com",
            "password": "Myp4$$wad!"

        }
        self.signin_payload1 = {
            "email": self.signup_payload1.get('email'),
            "password": self.signup_payload1.get('password')

        }

    def sign_up(self):
        with self.client as c:
            response = c.post(self.signup_url,
                              json=self.signup_payload0,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))
        return result

    def sign_up_non_admin(self):
        """Sign up a regular user"""
        with self.client as c:
            response = c.post(self.signup_url,
                              json=self.signup_payload1,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))
        return result

    def login(self):
        """Sign in the admin user"""
        self.sign_up()
        with self.client as c:
            response = c.post(self.signin_url,
                              json=self.signin_payload0,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

        return result

    def login_non_admin(self):
        """Sign in a regular user"""
        self.sign_up_non_admin()
        with self.client as c:
            response = c.post(self.signin_url,
                              json=self.signin_payload1,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

        return result

    def create_meetup(self):
        """Initialize a meetup"""
        self.sign_up()
        signin_result = self.login()
        with self.client as c:
            meetup_payload = {
                "topic": "Bootcamp Andela 36",
                "location": "PAC, Nairobi",
                "happeningOn": "2019-02-02 2:00pm",
                "tags": ["Bootcamp, Self-Learning"]
            }
            self.headers.update({"x-access-token": signin_result['token']})
            response = c.post('/api/v2/meetups',
                              json=meetup_payload,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

            return result

    def post_question(self):
        """Initialize a question post in a meetup"""
        self.sign_up()
        login_response = self.login()
        result = self.create_meetup()
        meetup_id = result['data']['id']
        print(result)

        self.headers.update({"x-access-token":
                             login_response['token']})
        question_payload = {
            "title": "How to train your dragon?",
            "body": "How does one get to tame their dragons?"
                    " Mine just ate my neighbors",
            "meetup": meetup_id
        }
        with self.client as c:
            question_post_response = c.post('api/v2/questions',
                                            json=question_payload,
                                            headers=self.headers)
            result = json.loads(question_post_response.data.decode('utf-8'))

            return [question_post_response, login_response['token']]

    def tearDown(self):
        """Tear down function called after every test"""
        self.client = None
        tables_tear_down(self.app)
