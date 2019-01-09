"""Test user sign up and authentication class"""

from .base_test import BaseTest
import datetime
import json

class TestAuths(BaseTest):
    """Tests for User Auths."""

    def test_signup(self):
        """Test for user signup."""
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            signup_data0 = {
                "id": 1,
                "firstname": "Joe",
                "lastname": "Waithaka",
                "password": "password",
                "othername": "",
                "email": "test@gmail.com",
                "phoneNumber": "254722222222",
                "username": "waithaka",
                "registered": datetime.datetime.now().strftime("%I:%M%p %d %b %Y"),
                "isAdmin": "False",
                }
            signup_response = c.post('/api/v1/signup', json=signup_data0, headers=headers)
            result = json.loads(signup_response.data.decode('utf-8'))
            self.assertEqual(result["message"], "User Created Successfully!")

            self.assertEqual(result["status"], signup_response.status_code)
            # self.assertEqual(signup_response.data.content_type, self.mime_type)

    def signup_missing_fields(self):
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            date = str(datetime.datetime.now().strftime("%I:%M%p %d %b %Y"))
            signup_data0 = {
                "id": 1,
                "firstname": "Joe",
                "lastname": "",
                "othername": "",
                "email": "test@gmail.com",
                "phoneNumber": "254722222222",
                "username": "waithaka",
                "registered": date,
                "isAdmin": False,
            }
            signup_response = c.post('/signup', json=signup_data0, headers=headers)
            result = json.loads(signup_response.data.decode('utf-8'))

            self.assertEqual(result["status"], 400)
            self.assertEqual(result["message"], "Missing Fields!")
            self.assertEqual(signup_response.data.content_type, self.mime_type)
