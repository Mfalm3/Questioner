"""Test for Meetups."""
from .base_test import BaseTest
import json
import datetime


class TestMeetup(BaseTest):
    """Test class for meetups."""

    def test_get_meetups(self):
        with self.client as c:
            headers = {"Content-Type": self.mime_type}
            meetups_response = c.get('/api/v1/meetups/upcoming', headers=headers)
            response = json.loads(meetups_response.data.decode('utf-8'))

            self.assertEqual(meetups_response.status_code, 200)
            self.assertEqual(response['status'], 200)
            self.assertIn("data", response)

    def test_create_meetup(self):
        with self.client as c:
            self.user1 = {
                "id": 1,
                "firstname": "Joe",
                "lastname": "Waithaka",
                "password": "password",
                "othername": "JW",
                "email": "test@gmail.com",
                "phoneNumber": "254722222222",
                "username": "waithaka",
                "registered": datetime.datetime.now().strftime("%I:%M%p %d %b %Y"),
                "isAdmin": "True",
            }
            login_payload = {
                "email": self.user1['email'],
                "password": self.user1['password']
            }
            meetup_payload = {
                    "topic": "Bootcamp",
                    "location": "Andela",
                    "happeningOn": "2:00pm 6th Feb 2019",
                    "tags": "django,flask"
                    }
            headers = {"Content-Type": self.mime_type}
            signup = c.post('/api/v1/signup', json=self.user1, headers=headers)
            login = c.post('/api/v1/login', json=login_payload, headers=headers)
            login_resp = json.loads(login.data.decode('utf-8'))

            self.assertIn("token", login_resp)

            token = login_resp['token']
            header_extra = {
                            "Content-type": self.mime_type,
                            "X-ACCESS-TOKEN": token
                            }

            post_meetup = c.post('/api/v1/meetups', json=meetup_payload, headers=header_extra)
            meetup_res = json.loads(post_meetup.data.decode('utf-8'))

            self.assertEqual(meetup_res['message'], "Meetup created successfully!")
