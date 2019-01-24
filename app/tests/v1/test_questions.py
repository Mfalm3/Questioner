"""Tests for questions"""
import unittest
import json
from app import create_app


class TestQuetions(unittest.TestCase):
    """Tesc class for questions"""

    def setUp(self):
        """Set up configs for question tests"""
        self.client = create_app('testing').test_client()
        self.admin_user = {
            "firstname": "J",
            "lastname": "Waithaka",
            "password": "password",
            "othername": "JW",
            "email": "sa.h@gmail.com",
            "phoneNumber": "254722222222",
            "username": "waithakaa",
            "registered": "now",
            "isAdmin": "True"
        }
        self.signin_payload = {
            "password": self.admin_user['password'],
            "email": self.admin_user['email']
        }
        self.meetup_payload = {
            "topic":  "Bootcamp 36 retreat",
            "location": "Andela Nairobi",
            "happeningOn": "2:00pm 6th Feb 2019",
            "tags": ["django", "flask"]
            }
        self.question_payload0 = {
            "title": "How to train your dragon",
            "meetup": "1",
            "body": "What are the basic requirements that one " \
            "needs when one training their dragon?",
            "createdBy": "123"
}

    def tearDown(self):
        """Tear down configs for question tests"""
        self.client = None

    def test_post_question(self):
        """Test for posting a question"""
        # sign up
        with self.client as c:
            headers = {"Content-type": 'application/json'}
            self.meetup_payload = {
                "topic": "Bootcamp and workshops",
                "location": "Andela, Nairobi",
                "happeningOn": "2:00pm 6th Feb 2019",
                "tags": ["django,flask"]
                    }
            signup_repsonse = c.post('api/v1/signup',
                                     json=self.admin_user,
                                     headers=headers)
            result0 = json.loads(signup_repsonse.data.decode('utf-8'))
            self.assertEqual(result0['message'], "User Created Successfully!")

        # log in
        with self.client as c:
            siginin_response = c.post("/api/v1/login",
                                      json=self.signin_payload,
                                      headers=headers)
            result1 = json.loads(siginin_response.data.decode('utf-8'))
            self.assertEqual(result1['message'], "Logged in successfully!")
            self.assertIn("token", result1)

        token = result1['token']
        header_extra = {
            "Content-type": "application/json",
            "X-ACCESS-TOKEN": token
        }

        # create meetup_
        with self.client as c:
            postmeetup_response = c.post("/api/v1/meetups",
                                         json=self.meetup_payload,
                                         headers=header_extra)
            result1 = json.loads(postmeetup_response.data.decode('utf-8'))
            self.assertEqual(result1['message'],
                             "Meetup created successfully!")

        # post question
        with self.client as c:
            postmeetup_question_response = c.post("/api/v1/questions",
                                                  json=self.question_payload0,
                                                  headers=header_extra)
            result1 = json.loads(postmeetup_question_response.data.decode('utf-8'))
            self.assertEqual(result1['message'],
                             "Question posted successfully!")
