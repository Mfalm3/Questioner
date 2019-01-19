"""Set up database connection"""
import psycopg2 as pg2
from instance.config import DevelopmentConfig, TestingConfig

DATABASE_LINKS = {
    'testing': TestingConfig.DATABASE_TEST_URL,
    'development': DevelopmentConfig.DATABASE_URL
}


def conn_link(link):
    """Creating a connection"""
    conn = pg2.connect(link)
    return conn


def init_dbase(url=None):
    """Initialize the database"""
    if url is None:
        link = DATABASE_LINKS['development']
    elif url == "testing":
        link = DATABASE_LINKS['development']
    conn = conn_link(link)
    cur = conn.cursor()
    db_queries = tables_setup()

    for table_query in db_queries:
        cur.execute(table_query)
    conn.commit()
    return conn


def tables_setup():
    """Defining the tables"""
    tables = []

    table0 = "CREATE TABLE IF NOT EXISTS users " \
             "(user_id serial PRIMARY KEY NOT NULL, " \
             "firstname character varying(32) NOT NULL, " \
             "lastname character varying(32) NOT NULL, " \
             "othername character varying(32), " \
             "email character varying(32) NOT NULL UNIQUE, " \
             "password character varying(256) NOT NULL, " \
             "phoneNumber character varying(16) NOT NULL, " \
             "username character varying(16) NOT NULL UNIQUE, " \
             "isAdmin boolean, " \
             "registered TIMESTAMP);"""

    table1 = "CREATE TABLE IF NOT EXISTS meetups " \
             "(meetup_id serial PRIMARY KEY, " \
             "meetup_topic character varying(64) NOT NULL UNIQUE, " \
             "meetup_location character varying (64) NOT NULL, " \
             "meetup_date DATE NOT NULL DEFAULT CURRENT_DATE, " \
             "meetup_tags character varying(50) NOT NULL );"

    table2 = "CREATE TABLE IF NOT EXISTS meetup_questions " \
             "(question_id serial PRIMARY KEY NOT NULL, " \
             "meetup_id INTEGER REFERENCES meetups(meetup_id), " \
             "user_id INTEGER REFERENCES users(user_id), " \
             "question_title character varying(64) NOT NULL, " \
             "question_body character varying(256) NOT NULL, " \
             "question_votes INTEGER NOT NULL); "

    table3 = "CREATE TABLE IF NOT EXISTS meetup_questions_comments " \
             "(comment_id serial PRIMARY KEY, " \
             "question_id INTEGER REFERENCES meetups_questions(question_id), " \
             "comment_body character varying(128));"

    tables.extend([table0, table1, table2, table3])
    return tables


def tables_tear_down():
    """Initialize test teardowns"""
    tears = []
    users = " DROP TABLE IF EXISTS users CASCADE"
    meetups = " DROP TABLE IF EXISTS meetups CASCADE"
    questions = " DROP TABLE IF EXISTS meetup_questions CASCADE"
    comments = " DROP TABLE IF EXISTS meetup_questions_comments CASCADE"
    tears.extend([users, meetups, questions, comments])
    conn = conn_link(DATABASE_LINKS['testing'])
    cur = conn.cursor()
    try:
        for tear in tears:
            cur.execute(tear)
            conn.commit()
    except Exception as e:
        print(e)
    return conn
