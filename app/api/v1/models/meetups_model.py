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
