# Validators
import re
from app.db import init_dbase


def valid_email(email):
    """Check if an email matches a regex pattern."""
    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)", email):
        local_part = email.split('@')[0]
        if re.match("^\\w+(\\d?)(\\.+(\\w|\\d))?$", local_part):
            return True
        return False


def check_if_exists(table='', column='', data=''):
    """Check if a given record exists in the database"""
    sql = """
    SELECT * from {} WHERE {} = '{}' LIMIT 1;
    """.format(table, column, data)

    conn = init_dbase()
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    if row:
        return True
    return False
