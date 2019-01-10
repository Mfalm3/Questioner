"""Tests For Voting."""
import json
from .base_test import BaseTest


class TestVoting(BaseTest):
    """Test class for up/down voting questions."""

    def test_upvoting(self):
        """Test for upvoting."""
        with self.client as c:
            headers = {"Content-type": "application/json"}
            upvote_response = c.patch('/api/v1/questions/1/upvote', headers=headers)
            result = json.loads(upvote_response.data.decode('utf-8'))

            # self.assertEqual(result['question']['votes'], 1)

    def test_downvoting(self):
        """Test for downvoting."""
        with self.client as c:
            headers = {"Content-type": "application/json"}
            downvote_response = c.patch('/api/v1/questions/1/downvote', headers=headers)
            result = json.loads(downvote_response.data.decode('utf-8'))

            self.assertEqual(result['question']['votes'], -1)
