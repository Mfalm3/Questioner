""" Question Model v2."""
from app.api.v2.models.base_model import BaseModel
from app.db import database_transactions


class QuestionModel(BaseModel):
    """Question model class."""

    def __init__(self, title, body, meetup, user):
        """Initialize the question instance"""
        super(QuestionModel, self).__init__()

        self.title = title
        self.body = body
        self.meetup = meetup
        self.user = user

    def save(self):
        """Save a new question to the database"""
        sql = """
        INSERT INTO meetup_questions (meetup_id,
        user_id, question_title, question_body)
        VALUES ('{}','{}','{}','{}')
        """.format(self.meetup, self.user, self.title, self.body)

        database_transactions(sql)
        data = {
            "topic": self.title,
            "body": self.body,
            "meetup": self.meetup,
            "user": self.user
        }
        return data

    @staticmethod
    def get_question(question_id):
        """Get a question in the database using id"""
        sql = """
        SELECT
        question_id, meetup_id, question_title, question_body, user_id,
        (
        (SELECT coalesce((select count(*) as votes from votes_table
        WHERE question_id = {} and action = 'upvote'
        GROUP BY action),0)as votes)
        -
        (SELECT coalesce((select count(*) as votes from votes_table
        WHERE question_id =1 and action = 'downvote'
        GROUP BY action),0)as votes)
        )as question_votes
        FROM meetup_questions WHERE question_id = '{}';
        """.format(question_id, question_id)
        data = database_transactions(sql)
        question = data.fetchone()
        if not question:
            return False
        return question

    @staticmethod
    def vote(vote_type, user_id, question_id):
        """upvote/downvote a question"""
        vote_exists = """
        SELECT * FROM votes_table WHERE user_id = {} AND question_id = {}
        """.format(user_id, question_id)
        has_voted = database_transactions(vote_exists)
        if not has_voted.fetchone():
            new_vote = """
            INSERT INTO votes_table (user_id, question_id, action)
            VALUES({}, {}, '{}')
            """.format(user_id, question_id, vote_type)
            database_transactions(new_vote)
        update_vote = """
        UPDATE votes_table SET action = '{}'
        """.format(vote_type)
        database_transactions(update_vote)

    @staticmethod
    def check_has_voted(user_id, question_id, vote_type):
        """Check if a user has already voted"""
        sql = """
        SELECT * FROM votes_table WHERE user_id = '{}'
        and
        question_id = '{}'
        and
        action = '{}';
        """.format(user_id, question_id, vote_type)
        data = database_transactions(sql)
        if data.fetchone():
            return True
        return False
