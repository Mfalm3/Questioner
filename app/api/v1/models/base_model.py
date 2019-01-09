"""Base model class"""

from app.db import init_db


class BaseModel(object):
    def __init__(self):
        self.db = init_db()