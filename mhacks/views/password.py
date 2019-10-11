"""
mhacks Password View.

URLs include:
/accounts/password/
"""
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.accountfunctions import check_login, hash_function


@mhacks.app.route('/accounts/password/', methods=['GET', 'POST'])
def password():
    """Save new password from user."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    if flask.request.method == 'POST':
        input_password = flask.request.form['password']
        input_new = flask.request.form['new_password1']
        input_new_2 = flask.request.form['new_password2']
        if not check_login(flask.session['username'], input_password):
            flask.abort(403)
        if input_new != input_new_2:
            flask.abort(401)
        if not check_password(input_new):
            flask.abort(400)

        hashed_password_new = hash_function(input_new)
        get_db().cursor().execute(''' UPDATE users SET password=?
                                  WHERE username=?''',
                                  (hashed_password_new,
                                   flask.session['username'],))
        return flask.redirect(flask.url_for('edit'))

    context = {}
    context["logname"] = flask.session["username"]
    return flask.render_template('password.html', **context)


def check_password(input_password):
    """Check if password is empty string."""
    if not input_password.strip():
        return False
    return True
