""" Meetups Model file."""
import datetime
import json
from app.api.v2.utils.utils import datetime_serializer
from app.api.v2.models.base_model import BaseModel
from app.db import database_transactions

time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M%P ")


class MeetupsModel(BaseModel):
    """Meetups Model."""

    def __init__(self, user_id, topic, location, happening_on, tags):
        """Initialize the Meetup model."""
        self.topic = topic
        self.location = location
        self.happening_on = happening_on
        self.tags = tags
        self.user_id = user_id
        self.created_at = json.dumps(time_stamp,
                                     default=datetime_serializer)

    def save(self):
        """Save meetup method"""
        sql = """
        INSERT INTO meetups (user_id, meetup_topic, meetup_location,
        meetup_date, meetup_tags, created_at)
        VALUES ( '{}', '{}', '{}', '{}', '{}', '{}' ) returning meetup_id;
        """.format(self.user_id, self.topic, self.location, self.happening_on,
                   self.tags, self.created_at)
        id = database_transactions(sql)

        data = {
            "id": id.fetchone()['meetup_id'],
            "topic": self.topic,
            "location": self.location,
            "happening_on": self.happening_on,
            "tags": self.tags
        }
        return data

    @staticmethod
    def get_upcoming():
        """Get upcoming meetup records."""
        sql = """
        SELECT * FROM meetups WHERE meetup_date > now() + interval '1 day';
        """
        cur = database_transactions(sql)
        data = cur.fetchall()

        return data
