"""Test for error handling"""
import json
import datetime
from .base_test import BaseTest


class TestStatusCodes(BaseTest):
    """Test class for error handlers"""

    def test_error_405(self):
        """Test for error status code 405"""
        with self.client as c:
            signup_request = c.get('/api/v1/signup')
            signup_response = json.loads(signup_request.data.decode('utf-8'))

            self.assertEqual(signup_response['status'], 405)
            self.assertEqual(signup_response['error'],
                             "405 Method Not Allowed: The method is not allowed for the requested URL.")

    def test_error_404(self):
        """Test for error status code 404"""
        with self.client as c:
            signup_request = c.post('/api/v1/signu')
            signup_response = json.loads(signup_request.data.decode('utf-8'))

            self.assertEqual(signup_response['status'], 404)
            self.assertEqual(signup_response['error'],
                             "404 Not Found: The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.")

    def test_error_403(self):
        """Test error 403 in creating a new meetup"""
        with self.client as c:

            headers = {"Content-Type": self.mime_type}
            timestamp = datetime.datetime.now().strftime("%I:%M%p %d %b %Y")
            self.user_non_admin = {
                "id": 1,
                "firstname": "User",
                "lastname": "Two",
                "password": "password",
                "othername": "JW",
                "email": "tester@gmail.com",
                "phoneNumber": "254722222222",
                "username": "test",
                "registered": timestamp,
                "isAdmin": "False",
            }
            self.login_payload_non_admin = {
                "email": self.user_non_admin['email'],
                "password": self.user_non_admin['password']
            }
            c.post('/api/v1/signup',
                   json=self.user_non_admin,
                   headers=headers)
            login = c.post('/api/v1/login',
                           json=self.login_payload_non_admin,
                           headers=headers)
            login_resp = json.loads(login.data.decode('utf-8'))

            self.assertIn("token", login_resp)

            token = login_resp['token']
            header_extra = {
                "Content-type": self.mime_type,
                "X-ACCESS-TOKEN": token
                }

            post_meetup = c.post('/api/v1/meetups',
                                 json=self.meetup_payload,
                                 headers=header_extra)
            meetup_res = json.loads(post_meetup.data.decode('utf-8'))

            self.assertEqual(meetup_res['error'],
                             "Action requires Admin Priviledges")
