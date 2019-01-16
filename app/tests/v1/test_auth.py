""" Test user sign up and authentication class."""
import unittest
import datetime
import json
from app import create_app


class TestAuths(unittest.TestCase):
    """Tests for User Auths."""

    def setUp(self):
        """Test set up."""
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
        self.user2 = {
            "id": 2,
            "firstname": "Jose",
            "lastname": "Wainaina",
            "password": "pw",
            "othername": "JW",
            "email": "test2@gmail.com",
            "phoneNumber": "254722333333",
            "username": "Wainaina",
            "registered": datetime.datetime.now().strftime("%I:%M%p %d %b %Y"),
            "isAdmin": "False",
        }

    def tearDown(self):
        """Test tear down"""
        self.client = None
        self.user1 = None

    def test_signup(self):
        """Test for user signup."""
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            signup_response = c.post('/api/v1/signup',
                                     json=self.user2,
                                     headers=headers)
            result = json.loads(signup_response.data.decode('utf-8'))
            self.assertEqual(result["message"], "User Created Successfully!")

            self.assertEqual(result["status"], signup_response.status_code)

    def test_signup_missing_fields(self):
        """Test for sign in with a missing field"""
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            date = str(datetime.datetime.now().strftime("%I:%M%p %d %b %Y"))
            signup_data0 = {
                "id": 1,
                "firstname": "Joe",
                "lastname": "",
                "password": "password",
                "othername": "",
                "email": "test@gmail.com",
                "phoneNumber": "254722222222",
                "username": "waithaka",
                "registered": date,
                "isAdmin": "False",
            }
            signup_response = c.post('/api/v1/signup',
                                     json=signup_data0,
                                     headers=headers)
            result = json.loads(signup_response.data.decode('utf-8'))

            self.assertEqual(result["status"], 400)
            self.assertEqual(result["error"], "lastname is missing.")

    def test_signup_dots_email_field(self):
        """Test for sign in with a missing field"""
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            date = str(datetime.datetime.now().strftime("%I:%M%p %d %b %Y"))
            signup_data1 = {
                "id": 1,
                "firstname": "Joe",
                "lastname": "Wa",
                "password": "password",
                "othername": "",
                "email": "...@gmail.com",
                "phoneNumber": "254722222222",
                "username": "waithaka",
                "registered": date,
                "isAdmin": "False",
            }
            signup_response = c.post('/api/v1/signup',
                                     json=signup_data1,
                                     headers=headers)
            result = json.loads(signup_response.data.decode('utf-8'))

            self.assertEqual(result["status"], 400)
            self.assertEqual(result["error"], "Ensure your email is in" \
                             " the right format! eg. test@example.com")

    def test_signup_no_json(self):
        """Test for user sign in with no data"""
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            response = c.post('/api/v1/signup', headers=headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(result['error'], "Please provide the required" \
                             " fields. ['firstname', 'lastname', 'password',"\
                             " 'email', 'phoneNumber', 'username', 'isAdmin']")

    def test_signin(self):
        """Test for user sign in."""
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            response = c.post('/api/v1/signup',
                              headers=headers,
                              json=self.user1)
            result = json.loads(response.data.decode('utf-8'))

            email = result['user']['email']

            self.assertEqual(email, "test@gmail.com")
            data = {
                "email": email,
                "password": "password"
            }

            response2 = c.post('api/v1/login', json=data, headers=headers)
            result2 = json.loads(response2.data.decode('utf-8'))

            self.assertIsNotNone(result2['token'])
            self.assertEqual(result2['message'], "Logged in successfully!")

    def test_signin_user_not_exist(self):
        """Test for user does not exist."""
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            response = c.post('/api/v1/login',
                              headers=headers,
                              json=self.user2)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(result['error'],
                             "No user found with the given credentials")
