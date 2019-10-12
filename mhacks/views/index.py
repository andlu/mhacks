"""
mhacks index (main) view.

URLs include:
/
"""
import flask
import mhacks


@mhacks.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Show Signup or Login page."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('home')) # Need to fix redirect
    # handling post request
    if flask.request.method == 'POST':
        if 'log-in' in flask.request.form:
            flask.redirect(flask.url_for('login'))
        elif 'sign-up' in flask.request.form:
            flask.redirect(flask.url_for('create_user'))

    return flask.render_template("index.html")
