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
        # Delete profile picture
        table2 = get_db().cursor().execute(''' SELECT * FROM users
                                           WHERE username=?''',
                                           (flask.session['username'],))
        profile_pic = table2.fetchone()
        picture = profile_pic['filename']
        path2 = mhacks.app.config['UPLOAD_FOLDER'] + '/' + picture
        os.remove(path2)

        # Delete Photos
        # Find all post photos
        table = get_db().cursor().execute(''' SELECT * FROM posts
                                          WHERE owner=?''',
                                          (flask.session['username'],))
        posts = table.fetchall()
        for post in posts:
            filename = post['filename']
            path = mhacks.app.config['UPLOAD_FOLDER'] + '/' + filename
            os.remove(path)

        # Delete Rows
        get_db().cursor().execute(''' DELETE FROM users
                                  WHERE username=? ''',
                                  (flask.session['username'],))
        flask.session.pop('username', None)
        return flask.redirect(flask.url_for('create'))

    context = {}
    context["logname"] = flask.session["username"]
    return flask.render_template('delete.html', **context)
