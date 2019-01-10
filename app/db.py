
db = []
user_db = []
meetup_db = [{
    "id": 1,
    "title": "Catching up with the world of JS",
    "location": "KCB sports club",
    "happeningOn": "10:00am 25 Jan 2019",
    "tags": ["VueJs", "ES2016"]
}]
question_db = [{
    "id": 1,
    "title": "Catching up with the world of JS",
    "body": "An exploration of the upcoming things in javascript trends",
    "meetup": 1,
    "createdOn": "12:12:43pm 9 Jan 2019",
    "createdBy": "waithaka",
    "votes": 0,
}]
comment_db = []
test_db = []


def init_db(db=db):
    database = db
    return database
