"""Test for Meetups."""
from .base_test import BaseTest
import json


class TestMeetups(BaseTest):
    """Test class for meetups."""

    def test_get_meetups(self):
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            meetups_response = c.get('/api/v1/meetups/upcoming', headers=headers)
            response = json.loads(meetups_response.data.decode('utf-8'))

            self.assertEqual(meetups_response.status_code, 200)
            self.assertEqual(response['status'], 200)
            self.assertIn("data", response)
