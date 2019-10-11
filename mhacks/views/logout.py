"""
mhacks Logout View.

URLs include:
/accounts/logout/
"""
import flask
import mhacks


@mhacks.app.route('/accounts/logout/')
def logout():
    """Logout User."""
    flask.session.pop('username', None)
    return flask.redirect(flask.url_for('login'))
