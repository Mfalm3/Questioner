""" Comments Model v2."""
from app.api.v2.models.base_model import BaseModel
from app.db import database_transactions


class CommentsModel(BaseModel):
    """Comments model class."""

    def __init__(self, question, title, body, comment, user):
        """Initialize the Comments instance"""
        super(CommentsModel, self).__init__()

        self.question = question
        self.title = title
        self.body = body
        self.comment = comment
        self.user = user

    def save(self):
        """Save a new comment to the database"""
        sql = """
        INSERT INTO meetup_questions_comments (question_id,
        question_title, user_id,  question_body, comment_body)
        VALUES ('{}','{}', '{}','{}','{}')
        """.format(self.question, self.title, self.user, self.body,
                   self.comment)

        database_transactions(sql)
        data = {
            "title": self.title,
            "body": self.body,
            "question": self.question,
            "comment": self.comment,
            "user": self.user
        }
        return data
