"""
mhacks Post View.

URLs include:
/p/<postid_slug>/
"""
import os
import flask
import arrow
from mhacks.model import get_db
import mhacks


@mhacks.app.route('/p/<postid_slug>/', methods=['GET', 'POST'])
def show_post(postid_slug):
    """Show a specific post."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # handling post request
    if flask.request.method == 'POST':
        # Stuff with like and comments
        if 'comment' in flask.request.form:
            text = flask.request.form['text']
            get_db().cursor().execute('''INSERT INTO
                                      comments(owner, postid, "text")
                                      VALUES (?, ?, ?) ''',
                                      (flask.session["username"],
                                       postid_slug, text,))
        elif 'unlike' in flask.request.form:
            check_unlike(flask.session['username'], postid_slug)

            get_db().cursor().execute('''DELETE FROM likes
                                      WHERE owner=? AND postid=?''',
                                      (flask.session["username"],
                                       postid_slug,))
        elif 'like' in flask.request.form:
            get_db().cursor().execute('''INSERT INTO
                                      likes(owner, postid)
                                      VALUES (?, ?)''',
                                      (flask.session["username"],
                                       postid_slug,))
        elif 'uncomment' in flask.request.form:
            commentid = flask.request.form['commentid']
            comment = get_db().cursor().execute('''SELECT * FROM comments
                                                WHERE commentid=?''',
                                                (commentid,)).fetchone()
            if flask.session['username'] != comment['owner']:
                flask.abort(403)
            get_db().cursor().execute('''DELETE FROM comments
                                      WHERE owner=? AND commentid=?''',
                                      (flask.session["username"],
                                       commentid,))
        elif 'delete' in flask.request.form:
            # deleting post pic
            del_postid = flask.request.form['postid']
            pic = get_db().cursor().execute('''SELECT * FROM posts
                                            WHERE postid=?''',
                                            (del_postid,)).fetchone()
            if flask.session['username'] != pic['owner']:
                flask.abort(403)
            get_db().cursor().execute('''DELETE FROM posts
                                      WHERE owner=? AND postid=?''',
                                      (flask.session["username"],
                                       del_postid,))
            pic_file = pic['filename']
            path = mhacks.app.config['UPLOAD_FOLDER'] + '/' + pic_file
            os.remove(path)
            temp = flask.session["username"]
            return flask.redirect(flask.url_for('show_user',
                                                user_url_slug=temp))
        else:
            # not sure if this is the right error
            flask.abort(403)
    # context for template
    context = {}
    context['logname'] = flask.session['username']
    context['postid'] = postid_slug
    owner = get_db().cursor().execute('''SELECT * FROM posts
                                      WHERE postid=?''',
                                      (postid_slug,)).fetchone()
    comments = get_db().cursor().execute('''SELECT *
                                         FROM comments WHERE postid=?''',
                                         (postid_slug,)).fetchall()
    likes = get_db().cursor().execute('''SELECT *
                                      FROM likes WHERE postid=?''',
                                      (postid_slug,)).fetchall()
    context['owner'] = owner['owner']
    context['img_url'] = owner['filename']
    context['likes'] = len(likes)
    context["did_like"] = False
    for i in likes:
        if i['owner'] == flask.session["username"]:
            context["did_like"] = True
    context['timestamp'] = arrow.get(owner['created']).humanize()
    context['comments'] = comments
    # get user propic
    propic = get_db().cursor().execute('''SELECT * FROM users
                                       WHERE username=?''',
                                       (owner['owner'],)).fetchone()
    context['owner_img_url'] = propic['filename']
    return flask.render_template("post.html", **context)
