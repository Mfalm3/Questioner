""" Base model class"""

from app.db import init_db


class BaseModel(object):
    """Base class model with bare shared across varous files"""

    def __init__(self):
        """Initialize the base model class"""
        self.db = init_db()
