"""Test for Meetups."""
from .base_test import BaseTest
import json


class TestMeetups(BaseTest):
    """Meetups Test class."""

    def test_post_question(self):
        """Test for posting question."""
        with self.client as c:
            headers = {"Content-type": 'application/json'}
            question = {
                "title": "How to train your dragon",
                "meetup": "1",
                "body": "What are the basic requirements that one needs when one training their dragon?",
                "createdBy": "waithaka"
            }
            post_response = c.post('/api/v1/meetups', json=question, headers=headers)
            result = json.loads(post_response.data.decode('utf-8'))

            self.assertEqual(result['status'], 201)
            self.assertEqual(result['message'], "Question posted successfully!")

    def test_post_question_with_missing_fields(self):
        """Testing for posting a question with missing fields."""
        with self.client as c:
            headers = {"Content-type": 'application/json'}
            question = {
                "title": "",
                "meetup": "1",
                "body": "What are the basic requirements that one needs when one training their dragon?",
                "createdBy": "waithaka"
            }
            post_response = c.post('/api/v1/meetups', json=question, headers=headers)
            result = json.loads(post_response.data.decode('utf-8'))

            self.assertEqual(result['error'], "title is missing.")
            self.assertEqual(result['status'], 400)
