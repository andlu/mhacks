"""
mhacks Explore View.

URLs include:
/explore/
"""
import flask
import mhacks
from mhacks.model import get_db


@mhacks.app.route('/explore/', methods=['GET', 'POST'])
def show_explore():
    """Show explore page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # handling post request
    if flask.request.method == 'POST':
        # follow stuff
        we_friends = flask.request.form['username']
        if 'follow' in flask.request.form:
            follow_friend(flask.session["username"], we_friends)
    # context for template
    context = {}
    context['logname'] = flask.session["username"]
    # find all users not following
    context['not_following'] = []
    following = get_db().cursor().execute('''SELECT * FROM following
                                          WHERE username1=?''',
                                          (flask.session["username"],)
                                          ).fetchall()
    list_following = []
    for i in following:
        list_following.append(i['username2'])
    list_following.append(flask.session['username'])
    context['not_following'] = []
    all_users = get_db().cursor().execute('''SELECT * FROM users''').fetchall()
    for i in all_users:
        if i['username'] not in list_following:
            context['not_following'].append(i)
    return flask.render_template("explore.html", **context)
