"""Test for user authentication"""
import json
from app.tests.v2.base_test import BaseTest


class TestUsers(BaseTest):
    """Users Auth test class"""

    def test_signup(self):
        """Test for user signup"""
        result = self.sign_up()

        self.assertEqual(result['message'],
                         "User `waithaka` created successfully!")

    def test_signup_with_existing_username(self):
        """Test for user signup with existing username"""
        with self.client as c:
            c.post(self.signup_url, json=self.signup_payload0,
                   headers=self.headers)
            response = c.post(self.signup_url,
                              json=self.signup_payload0,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(result['error'], "That username already exists!")

    def test_signup_with_existing_email(self):
        """Test for user signup with existing email"""
        with self.client as c:
            c.post(self.signup_url, json=self.signup_payload0,
                   headers=self.headers)
            self.signup_payload0['username'] = 'new_user'
            new_payload = self.signup_payload0
            response = c.post(self.signup_url,
                              json=new_payload,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(
                result['error'], "That email already exists."
                "Perhaps you want to login?")

    def test_signup_with_wrong_email(self):
        """Test for user signup with wrong email format"""
        with self.client as c:
            c.post(self.signup_url, json=self.signup_payload0,
                   headers=self.headers)
            self.signup_payload0['email'] = '...@gmail.com'
            new_payload = self.signup_payload0
            response = c.post(self.signup_url,
                              json=new_payload,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(
                result['error'], "The email provided is not in"
                " the right format")

    def test_with_missing_field(self):
        """Test for user signup with a missing field"""
        with self.client as c:
            c.post(self.signup_url, json=self.signup_payload0,
                   headers=self.headers)
            self.signup_payload0['firstname'] = ''
            new_payload = self.signup_payload0
            response = c.post(self.signup_url,
                              json=new_payload,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(result['error'], "firstname is missing.")

    def test_login(self):
        """Test for login"""
        result = self.login()

        self.assertEqual(result['message'], "Logged in successfully!")

    def test_login_with_non_existent_user(self):
        """Test for login with a user that has not been signed up"""
        with self.client as c:
            wrong_login_payload = {
                "email": "nonexistent@user.com",
                "password": "password"
            }
            response = c.post(self.signin_url,
                              json=wrong_login_payload,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            result['error'], "No user found with the given credentials")

    def test_login_with_wrong_password(self):
        """Test for a login with a wrong password"""
        self.sign_up()
        with self.client as c:
            wrong_login_password = {
                "email": self.signin_payload0.get('email'),
                "password": "wrongpassword"
            }
            response = c.post(self.signin_url,
                              json=wrong_login_password,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))
        print(wrong_login_password['email'])
        self.assertEqual(
            result['error'], "Password is invalid. Please check your"
            " credentials")

    def test_login_invalid_email(self):
        """Test for login with an invalid email format"""
        self.sign_up()
        with self.client as c:
            wrong_email_format = {
                "email": "...@gmail.com",
                "password": "password"
            }
            response = c.post(self.signin_url,
                              json=wrong_email_format,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            result['error'], "Email invalid")

    def test_token_generation_in_login(self):
        """Test if a token is being generated after login"""
        self.sign_up()
        result = self.login()

        self.assertIn("token", result)
