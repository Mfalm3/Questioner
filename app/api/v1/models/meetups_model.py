"""Meetups Model file."""
from .base_model import BaseModel, init_db
from app.db import meetup_db


class MeetupsModel(BaseModel):
    """Meetups Model."""

    def __init__(self):
        """Initialize the Meetup model."""
        self.db = init_db(meetup_db)

    def get_all(self):
        """Get all meetups."""
        meetups = self.db
        return meetups

    def get_meetup(self, meetup_id):
        """Get a specific meetup."""
        one_meetup = self.db[meetup_id - 1]
        return one_meetup
