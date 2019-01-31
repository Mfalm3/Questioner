# Validators
import re
from app.db import database_transactions


def valid_email(email):
    """Check if an email matches a regex pattern."""
    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)", email):
        local_part = email.split('@')[0]
        if re.match("^\\w+(\\d?)(\\.+(\\w|\\d))?$", local_part):
            return True
    return False


def is_empty(*args):
    """Check for empty strings"""
    items = [*args]
    for item in items:
        if isinstance(item, str):
            check_string = item.replace(" ", "")
            if check_string == "":
                return True
        if isinstance(item, list):
            for each in item:
                check_string = each.replace(" ", "")
                if check_string == "":
                    return True
    return False


def check_if_exists(table='', column='', data=''):
    """Check if a given record exists in the database"""
    sql = """
    SELECT * from {} WHERE {} = '{}' LIMIT 1;
    """.format(table, column, data)

    cur = database_transactions(sql)
    exists = cur.fetchone()
    if exists:
        return True
    return False


def validate_password(pw):
    """Password validator function"""
    state = True
    while state:
        if len(pw) < 6 or len(pw) > 12:
            break
        elif not re.search('[a-z]', pw):
            break
        elif not re.search('[A-Z]', pw):
            break
        elif not re.search('[0-9]', pw):
            break
        elif not re.search('[$#@]', pw):
            break
        elif re.search('[\\s]', pw):
            break
        else:
            validation = True

            state = False
            break

    if state:
        validation = False

    return validation


def contains_whitespace(string):
    """Checking if a sring has whitepaces"""
    if re.search('[\\s]', string):
        return True
    return False


def is_string(value):
    if isinstance(value, str):
        if value.isalpha():
            return True
    return False
