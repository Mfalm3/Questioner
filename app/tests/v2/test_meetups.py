"""Test for meetup"""
import json
from app.tests.v2.base_test import BaseTest


class TestMeetups(BaseTest):
    """Meetups Test class"""

    def test_create_meetup(self):
        """Test for creating a meetup"""
        self.sign_up()
        signin_result = self.login()
        with self.client as c:
            meetup_payload = {
                "topic": "Bootcamp Andela 36",
                "location": "PAC, Nairobi",
                "happeningOn": "2019-2-2 2:00pm",
                "tags": ["Bootcamp, Self-Learning"]
            }
            self.headers.update({"x-access-token": signin_result['token']})
            response = c.post('/api/v2/meetups',
                              json=meetup_payload,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(result['message'], "Meetup created successfully!")

    def test_create_meetup_normal_user(self):
        """Test for creating a meetup with a normal user"""
        self.sign_up_non_admin()
        signin_result = self.login_non_admin()
        with self.client as c:
            meetup_payload = {
                "topic": "Bootcamp Andela 36",
                "location": "PAC, Nairobi",
                "happeningOn": "2019-2-2 2:00pm",
                "tags": ["Bootcamp, Self-Learning"]
            }
            self.headers.update({"x-access-token": signin_result['token']})
            response = c.post('/api/v2/meetups',
                              json=meetup_payload,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(result['error'], "Action requires admin privilidges!")
        self.assertEqual(response.status_code, 403)

    def test_create_meetup_existing_topic(self):
        """Test for creating duplicate meetups"""
        self.sign_up()
        signin_result = self.login()
        with self.client as c:
            meetup_payload = {
                "topic": "Bootcamp Andela 36",
                "location": "PAC, Nairobi",
                "happeningOn": "2019-2-2 2:00pm",
                "tags": ["Bootcamp, Self-Learning"]
            }
            self.headers.update({"x-access-token": signin_result['token']})
            c.post('/api/v2/meetups',
                   json=meetup_payload,
                   headers=self.headers)
            response = c.post('/api/v2/meetups',
                              json=meetup_payload,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(result['error'],
                         "A meetup with that topic already exists!")
        self.assertEqual(response.status_code, 409)

    def test_create_meetup_missing_field(self):
        """Test for creating missing field"""
        self.sign_up()
        signin_result = self.login()
        with self.client as c:
            meetup_payload = {
                "topic": "   ",
                "location": "PAC, Nairobi",
                "happeningOn": "2019-2-2 2:00pm",
                "tags": ["Bootcamp, Self-Learning"]
            }
            self.headers.update({"x-access-token": signin_result['token']})
            c.post('/api/v2/meetups',
                   json=meetup_payload,
                   headers=self.headers)
            response = c.post('/api/v2/meetups',
                              json=meetup_payload,
                              headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(result['error'],
                         "topic field is missing")
        self.assertEqual(response.status_code, 400)

    def test_get_upcoming_meetups(self):
        with self.client as c:
            response = c.get('/api/v2/meetups/upcoming', headers=self.headers)
            result = json.loads(response.data.decode('utf-8'))

            self.assertEqual(result['data'], [])
            self.assertIsInstance(result['data'], list)

    def test_delete_meetup(self):
        # signup a test user
        self.sign_up()

        # log the user in
        login_response = self.login()

        # create a test meetup
        result = self.create_meetup()

        self.headers.update({"x-access-token":
                             login_response['token']})
        with self.client as c:
            delete_response = c.delete('api/v2/meetups/1',
                                       headers=self.headers)
            result = json.loads(delete_response.data.decode('utf-8'))

            self.assertEqual(result['message'], "Meetup deleted successfully!")
