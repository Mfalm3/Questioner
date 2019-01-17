"""Set up database connection"""
import psycopg2 as pg2
from instance.config import DevelopmentConfig, TestingConfig

db0 = []
user_db = []
meetup_db = []
question_db = []
comment_db = []
test_db = []


def init_db(db=db0):
    database = db
    return database

def conn_link(link):
    """Creating a connection"""
    conn = pg2.connect(link)
    return conn


def init_db():
    """Initialize the database"""
    link = DevelopmentConfig.DATABASE_URL
    conn = conn_link(link)
    cur = conn.cursor()
    return conn


def init_tests_db():
    """Initialize the tests tatabase"""
    link = TestingConfig.DATABASE_TEST_URL
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
             "email character varying(32) NOT NULL UNIQUE, " \
             "othername character varying(32), " \
             "username character varying(16) NOT NULL UNIQUE, " \
             "isAdmin boolean);"

    table1 = "CREATE TABLE IF NOT EXISTS meetups " \
             "(meetup_id serial PRIMARY KEY, " \
             "meetup_topic character varying(64) NOT NULL UNIQUE, " \
             "meetup_location character varying (64) NOT NULL, " \
             "meetup_date DATE NOT NULL, " \
             "meetup_tags character varying(50) NOT NULL );"

    table2 = "CREATE TABLE IF NOT EXISTS meetup_questions " \
             "(question_id serial PRIMARY KEY NOT NULL, " \
             "meetup_id INTEGER NOT NULL, " \
             "question_title character varying(64) NOT NULL, " \
             "question_body character varying(256) NOT NULL, " \
             "question_votes INTEGER NOT NULL); "

    table3 = "CREATE TABLE IF NOT EXISTS meetup_questions_comments " \
             "(comment_id serial PRIMARY KEY, " \
             "question_id INTEGER NOT NULL, " \
             "comment_body character varying(128));"

    tables.extend([table0, table1, table2, table3])
    return tables


def tables_tear_down():
    """Initialize test teardowns"""
    tears = []
    users = " DROP TABLE IF EXISTS users"
    meetups = " DROP TABLE IF EXISTS meetups"
    questions = " DROP TABLE IF EXISTS meetup_questions"
    comments = " DROP TABLE IF EXISTS meetup_questions_comments"
    tears.extend([users, meetups, questions, comments])
    conn = conn_link(TestingConfig.DATABASE_TEST_URL)
    cur = conn.cursor()
    try:
        for tear in tears:
            cur.execute(tear)
            conn.commit()
    except Exception as e:
        print(e)
