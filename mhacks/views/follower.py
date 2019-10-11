"""
mhacks Followers View.

URLs include:
/u/<user_url_slug>/followers/
"""
import flask
import mhacks
from mhacks.model import get_db
from mhacks.views.accountfunctions import follow_friend, unfollow_friend


@mhacks.app.route('/u/<user_url_slug>/followers/', methods=['GET', 'POST'])
def show_follower(user_url_slug):
    """Follower page for user."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # handling post request
    if flask.request.method == 'POST':
        # Stuff for follow/unfollow
        is_friends = flask.request.form['username']
        if 'follow' in flask.request.form:
            follow_friend(flask.session["username"], is_friends)
        elif 'unfollow' in flask.request.form:
            unfollow_friend(flask.session["username"], is_friends)
        else:
            # not sure if this is the right error
            flask.abort(403)
    # context for template
    context = {}
    context['logname'] = flask.session['username']
    # contain info for following
    followers = get_db().cursor().execute('''SELECT * FROM following
                                          WHERE username2=?''',
                                          (user_url_slug,)).fetchall()
    context['followers'] = []
    for i in followers:
        temp = {}
        temp['username'] = i['username1']
        user_info = get_db().cursor().execute('''SELECT * FROM users WHERE
                                              username=?''',
                                              (i['username1'],)).fetchone()
        temp['user_img_url'] = user_info['filename']
        friends = get_db().cursor().execute('''SELECT * FROM following WHERE
                                            username1=? AND username2=?''',
                                            (flask.session['username'],
                                             i['username1'],)).fetchone()
        if friends is None:
            temp['logname_follows_username'] = False
        else:
            temp['logname_follows_username'] = True
        context['followers'].append(temp)
    return flask.render_template("followers.html", **context)
