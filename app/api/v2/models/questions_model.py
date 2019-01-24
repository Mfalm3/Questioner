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
        user_id, question_title, question_body, question_votes)
        VALUES ('{}','{}','{}','{}','{}')
        """.format(self.meetup, self.user, self.title, self.body, 0)

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
        SELECT * FROM meetup_questions WHERE question_id = '{}';
        """.format(question_id)
        data = database_transactions(sql)
        question = data.fetchone()
        if not question:
            return False
        return question

    @staticmethod
    def vote(vote_type, user_id, question_id):
        """upvote/downvote a question"""

        if vote_type == "upvote":
            upvote = """
            UPDATE meetup_questions SET question_votes = question_votes+1
            WHERE question_id = {};
            """.format(question_id)
            has_voted = """
            INSERT INTO votes_table (user_id, question_id) VALUES({}, {})
            """.format(user_id, question_id)
            database_transactions([upvote, has_voted])
        elif vote_type == "downvote":
            downvote = """
            UPDATE meetup_questions SET question_votes = question_votes-1
            WHERE question_id = {};
            """.format(question_id)
            has_voted = """
            INSERT INTO votes_table (user_id, question_id) VALUES({}, {})
            """.format(user_id, question_id)
            database_transactions([downvote, has_voted])

    @staticmethod
    def check_has_voted(user_id, question_id):
        """Check if a user has already voted"""
        sql = """
        SELECT * FROM votes_table WHERE user_id = '{}' and question_id = '{}';
        """.format(user_id, question_id)
        data = database_transactions(sql)
        if data.fetchone():
            return True
        return False
