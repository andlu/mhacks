"""Account functions."""
import uuid
import hashlib
import flask
import mhacks
from mhacks.model import get_db


def check_login(username, input_password):
    """Check if login is valid."""
    table = get_db().cursor().execute(''' SELECT * FROM users
                                      WHERE username=?''', (username,))
    result = table.fetchone()
    if result is None:
        return False

    hashed_password = result['password']
    algorithm = hashed_password.split('$')[0]
    salt = hashed_password.split('$')[1]

    password_salted = salt + input_password
    mal = hashlib.new(algorithm)
    mal.update(password_salted.encode('utf-8'))
    check_hash = mal.hexdigest()
    if check_hash == hashed_password.split('$')[2]:
        return True
    return False


def hash_function(input_password):
    """Create and returns the hashed password."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + input_password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string
