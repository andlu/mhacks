"""
mhacks Login View.

URLs include:
/accounts/login/
"""
import flask
import mhacks
from mhacks.views.accountfunctions import check_login


@mhacks.app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    """Log in user."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('home'))

    if flask.request.method == 'POST':
        username = flask.request.form['username']
        input_password = flask.request.form['password']

        if check_login(username, input_password):
            flask.session["username"] = username
            return flask.redirect(flask.url_for('show_index'))
        flask.abort(403)

    return flask.render_template('login.html')
