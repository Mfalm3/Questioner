# File containing the validations for the app
import re


def valid_email(email):
    """Check if an email matches a regex pattern."""
    if(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email)):
        return True
    return False

def email_exists(email, db):
    """Check if email exists in database."""
    if any(row['email'] == email for row in db):
        return True
    return False


def username_exists(username, db):
    """Check if username exists in database."""
    for rows in db:
        if username in rows.values():
            return True
        return False
