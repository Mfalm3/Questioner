""" Users Model Class v2"""
from app.api.v2.models.base_model import BaseModel


class UsersModel(BaseModel):
    """Model class for users."""

    def __init__(self):
        """Initialize the users model."""
        super(UsersModel, self).__init__()
