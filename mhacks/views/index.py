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

    return flask.render_template("index.html")
