""" Meetups Model file."""
from app.api.v2.models.base_model import BaseModel


class MeetupsModel(BaseModel):
    """Meetups Model."""

    def __init__(self):
        """Initialize the Meetup model."""
        super(MeetupsModel, self).__init__()
