"""Test for Voting"""
import json
from app.tests.v2.base_test import BaseTest


class TestVoting(BaseTest):
    """Voting Test class"""

    def test_upvote_a_question(self):
        """Test for upvoting a question"""
        result = self.post_question()
        header = {"x-access-token": result[1]}

        with self.client as c:
            upvote_response = c.patch('api/v2/questions/1/upvote',
                                      headers=header)

            result = json.loads(upvote_response.data.decode('utf-8'))
            print(result)

            self.assertEqual(result['message'],
                             "Question upvoted successfully!")

    def test_upvote_continously(self):
        """Test for continuous voting"""
        result = self.post_question()
        header = {"x-access-token": result[1]}

        with self.client as c:
            c.patch('api/v2/questions/1/upvote', headers=header)
            upvote_response = c.patch('api/v2/questions/1/upvote',
                                      headers=header)

            result = json.loads(upvote_response.data.decode('utf-8'))
            print(result)

            self.assertEqual(result['error'],
                             "You can only vote once!")

    def test_downvote_a_question(self):
        """Test for upvoting a question"""
        result = self.post_question()
        header = {"x-access-token": result[1]}

        with self.client as c:
            upvote_response = c.patch('api/v2/questions/1/downvote',
                                      headers=header)

            result = json.loads(upvote_response.data.decode('utf-8'))
            print(result)

            self.assertEqual(result['message'],
                             "Question downvoted successfully!")

    def test_downvote_continously(self):
        """Test for continuous voting"""
        result = self.post_question()
        header = {"x-access-token": result[1]}

        with self.client as c:
            c.patch('api/v2/questions/1/downvote', headers=header)
            downvote_response = c.patch('api/v2/questions/1/downvote',
                                        headers=header)

            result = json.loads(downvote_response.data.decode('utf-8'))
            print(result)

            self.assertEqual(result['error'],
                             "You can only vote once!")
