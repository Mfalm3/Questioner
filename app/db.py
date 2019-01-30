"""Set up database connection"""
import datetime
from flask import current_app as app
from werkzeug.security import generate_password_hash
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor


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
    cur.execute(admin_setup())
    conn.commit()

    return conn


def database_transactions(query):
    """Function to handle all database transactions"""
    conn = init_dbase(app)
    cur = conn.cursor()

    if isinstance(query, list):
        for sql in query:
            cur.execute(sql)
            conn.commit()
    elif isinstance(query, str):
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
             "isAdmin boolean DEFAULT FALSE, " \
             "registered TIMESTAMP);"""

    table1 = "CREATE TABLE IF NOT EXISTS meetups " \
             "(meetup_id serial PRIMARY KEY, " \
             "user_id INTEGER, " \
             "meetup_topic character varying(64) NOT NULL UNIQUE, " \
             "meetup_location character varying (64) NOT NULL, " \
             "meetup_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE, " \
             "meetup_tags character varying(50) NOT NULL, " \
             "created_at character varying(50) NOT NULL, " \
             "FOREIGN KEY (user_id) REFERENCES users(user_id)  " \
             "ON DELETE CASCADE ON UPDATE CASCADE);"

    table2 = "CREATE TABLE IF NOT EXISTS meetup_questions " \
             "(question_id serial PRIMARY KEY NOT NULL, " \
             "meetup_id INTEGER, " \
             "user_id INTEGER, " \
             "question_title character varying(64) NOT NULL, " \
             "question_body character varying(256) NOT NULL, " \
             "question_votes INTEGER DEFAULT 0, " \
             "FOREIGN KEY (meetup_id) REFERENCES meetups(meetup_id)  " \
             "ON DELETE CASCADE ON UPDATE CASCADE," \
             "FOREIGN KEY (user_id) REFERENCES users(user_id)  " \
             "ON DELETE CASCADE ON UPDATE CASCADE" \
             "); "

    table3 = "CREATE TABLE IF NOT EXISTS meetup_questions_comments " \
             "(comment_id serial PRIMARY KEY, " \
             "question_id INTEGER, " \
             "user_id INTEGER, " \
             "comment_body character varying(128)," \
             "question_title character varying(128)," \
             "question_body character varying(128)," \
             "FOREIGN KEY (question_id) REFERENCES " \
             "meetup_questions(question_id)  " \
             "ON DELETE CASCADE ON UPDATE CASCADE" \
             ");"

    table4 = "CREATE TABLE IF NOT EXISTS blacklisted_tokens " \
             "(token_id serial PRIMARY KEY, " \
             " blacklisted_token character varying(256) NOT NULL); "

    table5 = "CREATE TABLE IF NOT EXISTS votes_table (" \
             "id serial PRIMARY KEY, " \
             "user_id INTEGER, " \
             "question_id INTEGER, " \
             "action character varying(10), " \
             "FOREIGN KEY (user_id) REFERENCES users(user_id) " \
             "ON DELETE CASCADE, " \
             "FOREIGN KEY (question_id) REFERENCES" \
             " meetup_questions(question_id) ON DELETE CASCADE ON"\
             " UPDATE CASCADE)"

    table6 = "CREATE TABLE IF NOT EXISTS rsvps_table ("\
             "id serial PRIMARY KEY, "\
             " user_id INTEGER," \
             " meetup_id INTEGER," \
             "rsvp_response character varying(5))"

    tables.extend([table0, table1, table2, table3, table4, table5, table6])
    return tables


def admin_setup():
    """Create an admin user"""
    setup_data = """INSERT INTO users (firstname, lastname, othername, email,
    password, phoneNumber, username, isAdmin, registered) VALUES
    ('Captain', 'Hook', 'TH', 'admin@email.com', '{}', '254722222222',
     'capitan', True, '{}') ON CONFLICT DO NOTHING;
    """.format(generate_password_hash('Myp4$$wad!'), datetime.datetime.now())
    return setup_data


def tables_tear_down(app):
    """Initialize test teardowns"""
    tears = []
    users = " DROP TABLE IF EXISTS users CASCADE"
    meetups = " DROP TABLE IF EXISTS meetups CASCADE"
    questions = " DROP TABLE IF EXISTS meetup_questions CASCADE"
    comments = " DROP TABLE IF EXISTS meetup_questions_comments CASCADE"
    votes = "DROP TABLE IF EXISTS votes_table CASCADE"
    blacklisted_token = " DROP TABLE IF EXISTS blacklisted_tokens CASCADE"
    tears.extend([users, meetups, questions, comments, votes,
                  blacklisted_token])
    conn = conn_link(app.config.get('DATABASE_URL'))
    cur = conn.cursor()
    try:
        for tear in tears:
            cur.execute(tear)
            conn.commit()
    except Exception as e:
        print(e)
