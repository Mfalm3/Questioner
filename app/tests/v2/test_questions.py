"""Test for Questions"""
import json
from app.tests.v2.base_test import BaseTest


class TestQuestions(BaseTest):
    """Questions Test class"""

    def test_post_question(self):
        """Post a question to a meetup test"""
        signup_response = self.sign_up()
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
        print(signup_response['data']['id'])

        with self.client as c:
            question_post_response = c.post('api/v2/questions',
                                            json=question_payload,
                                            headers=self.headers)
            result = json.loads(question_post_response.data.decode('utf-8'))

            self.assertEqual(result['message'],
                             "Question posted to meetup successfully!")

    def test_for_duplicate_question_post(self):
        """Post a duplicate question to a meetup test"""
        signup_response = self.sign_up()
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
        print(signup_response['data']['id'])

        with self.client as c:
            c.post('api/v2/questions', json=question_payload,
                   headers=self.headers)
            question_post_response = c.post('api/v2/questions',
                                            json=question_payload,
                                            headers=self.headers)
            result = json.loads(question_post_response.data.decode('utf-8'))

            self.assertEqual(result['error'],
                             "A Question with that title had already been"
                             " asked in that meetup!")

    def test_question_post_non_existent_meetup(self):
        """Post a question to a non existent meetup test"""
        signup_response = self.sign_up()
        login_response = self.login()
        result = self.create_meetup()

        self.headers.update({"x-access-token":
                             login_response['token']})
        question_payload = {
            "title": "How to train your dragon?",
            "body": "How does one get to tame their dragons?"
                    " Mine just ate my neighbors",
            "meetup": 50
        }
        print(signup_response['data']['id'])

        with self.client as c:
            c.post('api/v2/questions', json=question_payload,
                   headers=self.headers)
            question_post_response = c.post('api/v2/questions',
                                            json=question_payload,
                                            headers=self.headers)
            result = json.loads(question_post_response.data.decode('utf-8'))

            self.assertEqual(result['error'],
                             "That meetup for the meetup id passed is "
                             "currently not available")
