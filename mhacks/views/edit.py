"""
mhacks Edit View.

URLs include:
/accounts/edit/
"""
import os
import flask
from mhacks.model import get_db
import mhacks


@mhacks.app.route('/accounts/edit/', methods=['GET', 'POST'])
def edit():
    """Edit user information."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    if flask.request.method == 'POST':
        current_username = flask.session['username']

        input_name = flask.request.form['fullname']

        if input_name is not None:
            table = get_db().cursor().execute(''' UPDATE users SET fullname=?
                                              WHERE username=?''',
                                              (input_name, current_username,))
        
        return flask.redirect(flask.url_for('edit'))

    context = {}
    table2 = get_db().cursor().execute(''' SELECT * FROM users WHERE
                                       username=?''',
                                       (flask.session['username'],))
    profile_pic = table2.fetchone()
    context['logname'] = flask.session["username"]
    context['fullname'] = profile_pic['fullname']
    return flask.render_template('edit.html', **context)
