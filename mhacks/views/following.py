"""
mhacks Following View.

URLs include:
/u/<user_url_slug>/following/
"""
import flask
import mhacks
from mhacks.model import get_db


@mhacks.app.route('/u/<user_url_slug>/following/', methods=['GET', 'POST'])
def show_following(user_url_slug):
    """Display following page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # handling post request
    if flask.request.method == 'POST':
        # Stuff for follow/unfollow
        not_friends = flask.request.form['username']
        if 'follow' in flask.request.form:
            get_db().cursor().execute('''INSERT INTO
                                      following(username1, username2)
                                      VALUES (?, ?)''',
                                      (flask.session["username"],
                                       not_friends,))
        elif 'unfollow' in flask.request.form:
            get_db().cursor().execute('''DELETE FROM following
                                      WHERE username1=?
                                      AND username2=?''',
                                      (flask.session["username"],
                                       not_friends,))
        else:
            # not sure if this is the right error
            flask.abort(403)
    # context for template
    context = {}
    context['logname'] = flask.session['username']
    # contain info for following
    following = get_db().cursor().execute('''SELECT * FROM following
                                          WHERE username1=?''',
                                          (user_url_slug,)).fetchall()
    context['following'] = []
    for i in following:
        temp = {}
        temp['username'] = i['username2']
        user_info = get_db().cursor().execute('''SELECT * FROM users
                                              WHERE username=?''',
                                              (i['username2'],)).fetchone()
        temp['user_img_url'] = user_info['filename']
        friends = get_db().cursor().execute('''SELECT * FROM following
                                            WHERE username1=?
                                            AND username2=?''',
                                            (flask.session['username'],
                                             i['username2'],)).fetchone()
        if friends is None:
            temp['logname_follows_username'] = False
        else:
            temp['logname_follows_username'] = True
        context['following'].append(temp)
    return flask.render_template("following.html", **context)
