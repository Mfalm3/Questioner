""" Test for Meetups."""
import json
from .base_test import BaseTest


class TestMeetups(BaseTest):
    """Meetups Test class."""

    def test_post_question(self):
        """Test for posting question."""
        with self.client as c:
            headers = {"Content-type": 'application/json'}
            question = {
                "title": "How to train your dragon",
                "meetup": "1",
                "body": "What are the basic requirements that one needs when \
                one training their dragon?",
                "createdBy": "123"
            }
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

            post_meetup = c.post('/api/v1/meetups',
                                 json=self.meetup_payload,
                                 headers=header_extra)

            post_response = c.post('/api/v1/questions',
                                   json=question,
                                   headers=header_extra)
            result = json.loads(post_response.data.decode('utf-8'))

            self.assertEqual(result['status'], 201)
            self.assertEqual(result['message'],
                             "Question posted successfully!")

    def test_post_question_with_missing_fields(self):
        """Testing for posting a question with missing fields."""
        with self.client as c:
            headers = {"Content-type": 'application/json'}
            question = {
                "title": "",
                "meetup": "1",
                "body": "What are the basic requirements that one needs \
                when one training their dragon?",
                "createdBy": "waithaka"
            }
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

            c.post('/api/v1/meetups',
                                 json=self.meetup_payload,
                                 headers=header_extra)
            post_response = c.post('/api/v1/questions',
                                   json=question,
                                   headers=header_extra)
            result = json.loads(post_response.data.decode('utf-8'))

            self.assertEqual(result['error'], "title is missing.")
            self.assertEqual(result['status'], 400)

    def test_get_meetup(self):
        """Testing for gettin a single meetup."""
        with self.client as c:
            headers = {"Content-type": "application/json"}
            get_meetup = c.get('/api/v1/meetups/1', headers=headers)
            result = json.loads(get_meetup.data.decode('utf-8'))

            self.assertEqual(result['status'], 200)
