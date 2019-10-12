"""
mhacks Edit View.

URLs include:
/accounts/delete/
"""
import os
import flask
from mhacks.model import get_db
import mhacks


@mhacks.app.route('/accounts/delete/', methods=['GET', 'POST'])
def delete():
    """Delete logged in user."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    # Delete Account
    if flask.request.method == 'POST':
        # Delete Rows
        get_db().cursor().execute(''' DELETE FROM users
                                  WHERE username=? ''',
                                  (flask.session['username'],))

        flask.session.pop('username', None)
        return flask.redirect(flask.url_for('create'))

    context = {}
    context["logname"] = flask.session["username"]
    return flask.render_template('delete.html', **context)
