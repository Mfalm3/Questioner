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
    def delete(meetup_id):
        """Delete a meetup record"""
        sql = """
        DELETE FROM meetups WHERE meetup_id = {};
        """.format(meetup_id)
        meetup = MeetupsModel.get_meetup(meetup_id)
        if meetup:
            database_transactions(sql)

    @staticmethod
    def get_upcoming():
        """Get upcoming meetup records."""
        sql = """
       SELECT row_to_json(meets) as meetup
            FROM (SELECT *,
                 (SELECT coalesce(json_agg(qst), '[]'::json)
                  FROM(SELECT question_id, meetup_id, question_title,
                  question_body, user_id,
                  (
                  (SELECT coalesce((select count(*) as votes from votes_table
                  WHERE action = 'upvote' and question_id = mq.question_id
                  GROUP BY action),0)as votes)
                  -
                  (SELECT coalesce((select count(*) as votes from votes_table
                  WHERE action = 'downvote' and question_id = mq.question_id
                  GROUP BY action),0)as votes)
                  )as question_votes,
                              (SELECT coalesce(json_agg(qstc), '[]'::json)
                                  FROM(SELECT  *
                                  FROM meetup_questions_comments mqc
                               WHERE mq.question_id = mqc.question_id
                               )qstc) AS comments
                  FROM meetup_questions mq WHERE m.meetup_id = mq.meetup_id
                      )qst)
                 AS questions
              FROM meetups m)AS meets
              WHERE meetup_date > now() + interval '1 day';
        """
        cur = database_transactions(sql)
        data = cur.fetchall()

        return data

    @staticmethod
    def get_meetup(meetup_id):
        """Get a meetup record in the database using its id"""
        sql = """
        SELECT row_to_json(meets) as meetup
             FROM (SELECT *,
                  (SELECT coalesce(json_agg(qst), '[]'::json)
                   FROM(SELECT question_id, meetup_id, question_title,
                   question_body, user_id,
                   (
                   (SELECT coalesce((select count(*) as votes from votes_table
                   WHERE action = 'upvote' and question_id = mq.question_id
                   GROUP BY action),0)as votes)
                   -
                   (SELECT coalesce((select count(*) as votes from votes_table
                   WHERE action = 'downvote' and question_id = mq.question_id
                   GROUP BY action),0)as votes)
                   )as question_votes,
                               (SELECT coalesce(json_agg(qstc), '[]'::json)
                                   FROM(SELECT  *
                                   FROM meetup_questions_comments mqc
                                WHERE mq.question_id = mqc.question_id
                                )qstc) AS comments
                   FROM meetup_questions mq WHERE m.meetup_id = mq.meetup_id
                       )qst)
                  AS questions
               FROM meetups m)AS meets
        WHERE meetup_id = {};
        """.format(meetup_id)
        data = database_transactions(sql)
        meetup = data.fetchone()
        if not meetup:
            return False
        return meetup
