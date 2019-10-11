"""
mhacks Edit View.

URLs include:
/accounts/edit/
"""
import os
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.accountfunctions import file_upload


@mhacks.app.route('/accounts/edit/', methods=['GET', 'POST'])
def edit():
    """Edit user information."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    if flask.request.method == 'POST':
        current_username = flask.session['username']
        table = get_db().cursor().execute(''' SELECT * FROM users WHERE
                                          username=?''',
                                          (current_username,))
        result = table.fetchone()
        current_photo = result['filename']

        input_name = flask.request.form['fullname']
        input_email = flask.request.form['email']
        input_file = flask.request.files['file']

        if input_name is not None:
            table = get_db().cursor().execute(''' UPDATE users SET fullname=?
                                              WHERE username=?''',
                                              (input_name, current_username,))

        if input_email is not None:
            table = get_db().cursor().execute(''' UPDATE users SET email=?
                                              WHERE username=?''',
                                              (input_email, current_username,))

        if input_file is not None:
            path = mhacks.app.config["UPLOAD_FOLDER"] + '/' + current_photo
            os.remove(path)
            new_photo = file_upload(input_file)
            table = get_db().cursor().execute(''' UPDATE users SET filename=?
                                              WHERE username=?''',
                                              (new_photo, current_username,))

        return flask.redirect(flask.url_for('edit'))

    context = {}
    table2 = get_db().cursor().execute(''' SELECT * FROM users WHERE
                                       username=?''',
                                       (flask.session['username'],))
    profile_pic = table2.fetchone()
    context['profilePic'] = profile_pic['filename']
    context['logname'] = flask.session["username"]
    context['fullname'] = profile_pic['fullname']
    context['email'] = profile_pic['email']
    return flask.render_template('edit.html', **context)
