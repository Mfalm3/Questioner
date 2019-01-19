"""Tests for Authentications"""
import json
from app.tests.v2.base_test import BaseTest


class TestAuths(BaseTest):
    """Test class for Auths"""

    def test_signup(self):
        with self.client as c:
            headers = {"Content-type": self.mime_type}
            signup_response = c.post(
                self.signup_url, json=self.signup_payload0, headers=headers)

            result = json.loads(signup_response.data.decode('utf-8'))

            self.assertEqual(result['message'],
                             "User `waithaka` created successfully!")
