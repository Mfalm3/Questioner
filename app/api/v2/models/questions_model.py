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
