""" Meetups Model file."""
import datetime
from flask import jsonify
from app.db import meetup_db
from .base_model import BaseModel, init_db


class MeetupsModel(BaseModel):
    """Meetups Model."""

    def __init__(self):
        """Initialize the Meetup model."""
        super(MeetupsModel, self).__init__()
        self.db = init_db(meetup_db)

    def meetup(self, location, images, topic, happeningOn, tags):
        """Meetup object."""
        tstamp = datetime.datetime.now().strftime("%I:%M:%S%P %d %b %Y")
        meetup = {
            "id": len(self.db) + 1,
            "createdOn": tstamp,
            "location": location,
            "images": images,
            "topic": topic,
            "happeningOn": happeningOn,
            "tags": tags,
        }
        return meetup

    def create(self, meetup):
        """Create a new meetup."""
        return self.db.append(meetup)

    def get_all(self):
        """Get all meetups."""
        meetups = self.db
        return meetups

    def get_meetup(self, meetup_id):
        """Get a specific meetup."""
        one_meetup = self.db[meetup_id - 1]
        return one_meetup

    def rsvp(self, meetup, user, response):
        """RSVP object."""
        rsvp = {
            "meetup": meetup,
            "user": user,
            "response": response
        }
        return rsvp

    def create_rsvp(self, rsvp):
        """Create an rsvp to a meetup"""
        meetup = rsvp['meetup']
        topic = self.get_meetup(meetup)['topic']
        status = rsvp['response']
        return jsonify({
            "status": 201,
            "message": "RSVP created successfully!",
            "data": {
                "meetup": meetup,
                "topic": topic,
                "status": status
            }

        })
