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

    def test_get_question(self):
        """Test for getting a specific question record"""
        # signup a test user
        signup_response = self.sign_up()

        # log the user in
        login_response = self.login()

        # create a test meetup
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

        # create a test question
        with self.client as c:
            question_post_response = c.post('api/v2/questions',
                                            json=question_payload,
                                            headers=self.headers)
            result = json.loads(question_post_response.data.decode('utf-8'))

            self.assertEqual(result['message'],
                             "Question posted to meetup successfully!")

        # Get the newly created question
        with self.client as c:
            question_get_response = c.get('/api/v2/questions/1',
                                          headers=self.headers)
            result = json.loads(question_get_response.data.decode('utf-8'))

            self.assertIn("data", result)
            self.assertEqual(question_get_response.status_code, 200)

    def test_get_question_of_non_existent_question(self):
        """
        Test for getting a specific question record that does not exist
        """
        # signup a test user
        signup_response = self.sign_up()

        # log the user in
        login_response = self.login()

        # create a test meetup
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

        # create a test question
        with self.client as c:
            question_post_response = c.post('api/v2/questions',
                                            json=question_payload,
                                            headers=self.headers)
            result = json.loads(question_post_response.data.decode('utf-8'))

            self.assertEqual(result['message'],
                             "Question posted to meetup successfully!")

        # Get the newly created question
        with self.client as c:
            question_get_response = c.get('/api/v2/questions/12',
                                          headers=self.headers)
            result = json.loads(question_get_response.data.decode('utf-8'))

            self.assertIn("error", result)
            self.assertEqual(question_get_response.status_code, 404)
            self.assertEqual(result['error'],
                             "Could't find a question record with that id")
