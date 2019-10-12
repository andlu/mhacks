"""
mhacks Create View.

URLs include:
/accounts/create/
"""
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.accountfunctions import file_upload, hash_function


@mhacks.app.route('/accounts/create/', methods=['GET', 'POST'])
def create_user():
    """Create a User."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('edit'))

    if flask.request.method == 'POST':
        input_username = flask.request.form['username']
        input_password = flask.request.form['password']
        input_name = flask.request.form['fullname']
        input_email = flask.request.form['email']

        # Abort Checks
        if not check_username(input_username):
            flask.abort(409)

        if not check_password(input_password):
            flask.abort(400)

        hashed_password = hash_function(input_password)

        # FILE PORTION
        file = flask.request.files["file"]
        hashed_filename = file_upload(file)

        # Insert into database
        get_db().cursor().execute(''' INSERT INTO users
                                  (username, fullname, email,
                                  filename, password)
                                  VALUES (?, ?, ?, ?, ?) ''',
                                  (input_username, input_name,
                                   input_email,
                                   hashed_filename,
                                   hashed_password))
        flask.session['username'] = input_username
        return flask.redirect(flask.url_for('show_index'))

    return flask.render_template('create.html')


def check_username(input_username):
    """Check if username already exists."""
    table = get_db().cursor().execute(''' SELECT * FROM users
                                      WHERE username=?''',
                                      (input_username,))
    result = table.fetchone()
    if result is None:
        return True
    return False


def check_password(input_password):
    """Check if input_password is an empty string."""
    if not input_password.strip():
        return False
    return True