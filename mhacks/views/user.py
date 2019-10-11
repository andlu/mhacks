"""
mhacks User View.

URLs include:
/u/<user_url_slug>/
"""
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.accountfunctions import (file_upload,
                                             follow_friend, unfollow_friend)


@mhacks.app.route('/u/<user_url_slug>/', methods=['GET', 'POST'])
def show_user(user_url_slug):
    """Display user homepage."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # handling post request
    if flask.request.method == 'POST':
        # Stuff for follow/unfollow
        if 'follow' in flask.request.form:
            follow_friend(flask.session["username"], user_url_slug)
        elif 'unfollow' in flask.request.form:
            unfollow_friend(flask.session["username"], user_url_slug)
        elif 'create_post' in flask.request.form:
            pic = flask.request.files['file']
            hashed_filename = file_upload(pic)
            get_db().cursor().execute('''INSERT INTO posts(filename,
                                      owner)
                                      VALUES (?, ?)''',
                                      (hashed_filename,
                                       flask.session["username"],))
        else:
            # not sure if this is the right error
            flask.abort(403)
    # context for template
    context = {}
    context['logname'] = flask.session["username"]
    # adding user's info
    context['username'] = user_url_slug
    user_info = get_db().cursor().execute('''SELECT * FROM users
                                          WHERE username=?''',
                                          (user_url_slug,)).fetchone()
    context['fullname'] = user_info['fullname']
    # getting num of followers/following
    num_followers = get_db().cursor().execute('''SELECT * FROM following
                                              WHERE username2=?''',
                                              (user_url_slug,)).fetchall()
    context['followers'] = len(num_followers)
    num_following = get_db().cursor().execute('''SELECT * FROM following
                                              WHERE username1=?''',
                                              (user_url_slug,)).fetchall()
    context['following'] = len(num_following)
    # checking if user follows this user
    we_friend = get_db().cursor().execute('''SELECT * FROM following
                                          WHERE username1=? AND username2=?''',
                                          (flask.session["username"],
                                           user_url_slug,)).fetchone()
    if we_friend is None:
        context['logname_follows_username'] = False
    else:
        context['logname_follows_username'] = True
    # getting all the post
    context['posts'] = get_db().cursor().execute('''SELECT * FROM posts
                                                 WHERE owner=?''',
                                                 (user_url_slug,)).fetchall()
    return flask.render_template("user.html", **context)
