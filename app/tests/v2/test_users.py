"""Test for user authentication"""
import json
from app.tests.v2.base_test import BaseTest


class TestUsers(BaseTest):
    """Users Auth test class"""
    def test_signup(self):
        """Test for user signup"""
        with self.client as c:
            headers = {"Content-type": self.mime_type}
            response = c.post(self.signup_url,
                              json=self.signup_payload0,
                              headers=headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(result['message'],
                             "User `waithaka` created successfully!")

    def test_signup_with_existing_username(self):
        """Test for user signup with existing username"""
        with self.client as c:
            headers = {"Content-type": self.mime_type}
            c.post(self.signup_url, json=self.signup_payload0,
                   headers=headers)
            response = c.post(self.signup_url,
                              json=self.signup_payload0,
                              headers=headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(result['error'], "That username already exists!")

    def test_signup_with_existing_email(self):
        """Test for user signup with existing email"""
        with self.client as c:
            headers = {"Content-type": self.mime_type}
            c.post(self.signup_url, json=self.signup_payload0,
                   headers=headers)
            self.signup_payload0['username'] = 'new_user'
            new_payload = self.signup_payload0
            response = c.post(self.signup_url,
                              json=new_payload,
                              headers=headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(
                result['error'], "That email already exists."
                "Perhaps you want to login?")

    def test_signup_with_wrong_email(self):
        """Test for user signup with wrong email format"""
        with self.client as c:
            headers = {"Content-type": self.mime_type}
            c.post(self.signup_url, json=self.signup_payload0,
                   headers=headers)
            self.signup_payload0['email'] = '...@gmail.com'
            new_payload = self.signup_payload0
            response = c.post(self.signup_url,
                              json=new_payload,
                              headers=headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(
                result['error'], "The email provided is not in"
                " the right format")

    def test_with_missing_field(self):
        """Test for user signup with a missing field"""
        with self.client as c:
            headers = {"Content-type": self.mime_type}
            c.post(self.signup_url, json=self.signup_payload0,
                   headers=headers)
            self.signup_payload0['firstname'] = ''
            new_payload = self.signup_payload0
            response = c.post(self.signup_url,
                              json=new_payload,
                              headers=headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(
                result['error'], "firstname is missing.")
