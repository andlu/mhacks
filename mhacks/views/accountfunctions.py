"""Account functions."""
import uuid
import hashlib
import os
import shutil
import tempfile
import flask
import mhacks
from mhacks.model import get_db


def file_upload(file):
    """Save and returns hashed file name."""
    # Save POST request's file object to a temp file
    dummy, temp_filename = tempfile.mkstemp()
    file.save(temp_filename)

    # Compute filename
    hash_txt = sha256sum(temp_filename)
    dummy, suffix = os.path.splitext(file.filename)
    hash_filename_basename = hash_txt + suffix
    hash_filename = os.path.join(
        mhacks.app.config["UPLOAD_FOLDER"],
        hash_filename_basename
    )

    # Move temp file to permanent location
    shutil.move(temp_filename, hash_filename)
    mhacks.app.logger.debug("Saved %s", hash_filename_basename)
    return hash_filename_basename


def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


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


def follow_friend(logname, friend):
    """Logname follows account."""
    get_db().cursor().execute('''INSERT INTO following(username1, username2)
                              VALUES (?, ?)''', (logname, friend,))


def unfollow_friend(logname, not_friend):
    """Logname user is not following account."""
    get_db().cursor().execute('''DELETE FROM following WHERE username1=?
                              AND username2=?''', (logname, not_friend,))


def check_unlike(logname, postid):
    """Check if unlike is from session user."""
    like = get_db().cursor().execute(''' SELECT * FROM likes
                                     WHERE owner=? AND postid=? ''',
                                     (logname,
                                      postid,)).fetchone()
    if like is None:
        flask.abort(403)
