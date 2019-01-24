"""Test for Comments"""
import json
from app.tests.v2.base_test import BaseTest


class TestComments(BaseTest):
    """Comments Test class"""

    def test_post_comment(self):
        """Test for a user posting a comment to a question"""
        self.sign_up()
        login_response = self.login()
        result = self.create_meetup()
        meetup_id = result['data']['id']

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

        comment_payload =  {
            "body": "How does one get to tame their dragons?"
                    " Mine just ate my neighbors",
            "comment": "Put him on a leash",
            "question": 1,
            "title": "How to train your dragon?"
        }
        with self.client as c:
            question_post_response = c.post('api/v2/comments',
                                            json=comment_payload,
                                            headers=self.headers)
            result = json.loads(question_post_response.data.decode('utf-8'))

            self.assertEqual(result['message'],
                             "Comment added successfully")

    def test_post_comment_without_existing_question(self):
        """Test for posting a comment when the question doesn't exist"""
        self.sign_up()
        login_response = self.login()
        result = self.create_meetup()

        self.headers.update({"x-access-token":
                             login_response['token']})

        comment_payload = {
            "body": "How does one get to tame their dragons?"
                    " Mine just ate my neighbors",
            "comment": "Put him on a leash",
            "question": 1,
            "title": "How to train your dragon?"
        }
        with self.client as c:
            question_post_response = c.post('api/v2/comments',
                                            json=comment_payload,
                                            headers=self.headers)
            result = json.loads(question_post_response.data.decode('utf-8'))

            self.assertEqual(result['error'],
                             "Could not get the question for the id"
                             " passed in in that meetup!")
