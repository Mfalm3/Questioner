"""Set up database connection"""
import os
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
from flask import current_app as app


def conn_link(link):
    """Creating a connection"""
    try:
        conn = pg2.connect(link, cursor_factory=RealDictCursor)
    except Exception as error:
        return "Database connection error" + error
    return conn


def init_dbase(app):
    """Initialize the database"""
    url = app.config.get('DATABASE_URL')

    conn = conn_link(url)
    cur = conn.cursor()
    db_queries = tables_setup()

    for table_query in db_queries:
        cur.execute(table_query)
    conn.commit()
    return conn


def database_transactions(query):
    conn = init_dbase(app)
    if isinstance(query, list):
        for sql in query:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
    elif isinstance(query, str):
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

    return cur


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
             "question_id INTEGER REFERENCES meetup_questions(question_id), " \
             "comment_body character varying(128));"

    table4 = "CREATE TABLE IF NOT EXISTS blacklisted_tokens " \
             "(token_id serial PRIMARY KEY, " \
             " blacklisted_token character varying(256) NOT NULL); "

    tables.extend([table0, table1, table2, table3, table4])
    return tables


def tables_tear_down(app):
    """Initialize test teardowns"""
    tears = []
    users = " DROP TABLE IF EXISTS users CASCADE"
    meetups = " DROP TABLE IF EXISTS meetups CASCADE"
    questions = " DROP TABLE IF EXISTS meetup_questions CASCADE"
    comments = " DROP TABLE IF EXISTS meetup_questions_comments CASCADE"
    comments = " DROP TABLE IF EXISTS blacklisted_token CASCADE"
    tears.extend([users, meetups, questions, comments])
    conn = conn_link(app.config.get('DATABASE_URL'))
    cur = conn.cursor()
    try:
        for tear in tears:
            cur.execute(tear)
            conn.commit()
    except Exception as e:
        print(e)
