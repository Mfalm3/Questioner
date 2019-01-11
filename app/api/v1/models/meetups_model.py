"""Meetups Model file."""
import datetime
from .base_model import BaseModel, init_db
from app.db import meetup_db


class MeetupsModel(BaseModel):
    """Meetups Model."""

    def __init__(self):
        """Initialize the Meetup model."""
        self.db = init_db(meetup_db)

    def meetup(self, location, images, topic, happeningOn, tags):
        """Meetup object."""
        meetup = {
                    "id": len(self.db) + 1,
                    "createdOn": datetime.datetime.now().strftime("%I:%M:%S%P %d %b %Y"),
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
