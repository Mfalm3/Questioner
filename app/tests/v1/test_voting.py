""" Tests For Voting."""
import json
from .base_test import BaseTest


class TestVoting(BaseTest):
    """Test class for up/down voting questions."""

    def test_upvoting(self):
        """Test for upvoting."""
        with self.client as c:

            headers = {"Content-Type": self.mime_type}
            c.post('/api/v1/signup',
                   json=self.user0,
                   headers=headers)
            login = c.post('/api/v1/login',
                           json=self.login_payload1,
                           headers=headers)
            login_resp = json.loads(login.data.decode('utf-8'))

            self.assertIn("token", login_resp)

            token = login_resp['token']
            header_extra = {
                "Content-type": self.mime_type,
                "X-ACCESS-TOKEN": token
            }

            upvote_response = c.patch('/api/v1/questions/1/upvote',
                                 headers=header_extra)

            self.assertEqual(upvote_response.status_code, 200)

    def test_downvoting(self):
        """Test for downvoting."""
        with self.client as c:
            headers = {"Content-type": "application/json"}
            c.post('/api/v1/signup',
                   json=self.user1,
                   headers=headers)
            login = c.post('/api/v1/login',
                           json=self.login_payload,
                           headers=headers)
            login_resp = json.loads(login.data.decode('utf-8'))

            self.assertIn("token", login_resp)

            token = login_resp['token']
            header_extra = {
                "Content-type": self.mime_type,
                "X-ACCESS-TOKEN": token
            }

            downvote_response = c.patch('/api/v1/questions/1/downvote',
                                        headers=header_extra)
            result = json.loads(downvote_response.data.decode('utf-8'))

            self.assertEqual(result['question']['votes'], -1)
