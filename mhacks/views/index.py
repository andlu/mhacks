"""
mhacks index (main) view.

URLs include:
/
"""
import flask
import arrow
import mhacks
from mhacks.model import get_db
from mhacks.views.accountfunctions import check_unlike


@mhacks.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Show index page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # handling post request
    if flask.request.method == 'POST':
        # get what post the post request came from
        postid = flask.request.form['postid']
        # Stuff with like and comments
        if 'comment' in flask.request.form:
            text = flask.request.form['text']
            get_db().cursor().execute(''' INSERT INTO
                                      comments(owner, postid, "text")
                                      VALUES (?, ?, ?) ''',
                                      (flask.session["username"],
                                       postid, text,))
        elif 'unlike' in flask.request.form:
            check_unlike(flask.session['username'], postid)

            get_db().cursor().execute(''' DELETE FROM likes
                                      WHERE owner=? AND postid=? ''',
                                      (flask.session["username"],
                                       postid,))
        elif 'like' in flask.request.form:
            get_db().cursor().execute(''' INSERT INTO
                                      likes(owner, postid)
                                      VALUES (?, ?) ''',
                                      (flask.session["username"],
                                       postid,))
        else:
            # not sure if this is the right error
            flask.abort(403)
    # context for template
    context = {}
    context["logname"] = flask.session["username"]
    # contain info for following
    following = get_db().cursor().execute(''' SELECT * FROM following
                                          WHERE username1=?''',
                                          (flask.session["username"],)
                                          ).fetchall()
    context["posts"] = []
    # append post user is following
    for friend in following:
        all_post = get_db().cursor().execute(''' SELECT * FROM posts
                                             WHERE owner=?''',
                                             (friend["username2"],)
                                             ).fetchall()
        # get the user profile pic
        owner_img = get_db().cursor().execute(''' SELECT * FROM users
                                              WHERE username=?''',
                                              (friend["username2"],)
                                              ).fetchone()
        # append all the friend's post
        for post in all_post:
            post['owner_img_url'] = owner_img['filename']
            post['created'] = arrow.get(post['created']).humanize()
            context["posts"].append(post)
    # need to add own posts
    all_post = get_db().cursor().execute(''' SELECT * FROM posts
                                         WHERE owner=?''',
                                         (flask.session["username"],)
                                         ).fetchall()
    owner_img = get_db().cursor().execute(''' SELECT * FROM users
                                          WHERE username=?''',
                                          (flask.session["username"],)
                                          ).fetchone()
    for post in all_post:
        post['owner_img_url'] = owner_img['filename']
        post['created'] = arrow.get(post['created']).humanize()
        context["posts"].append(post)
    context["posts"].sort(key=post_ordering, reverse=True)
    # adding the likes and comments to the post dict
    for i in context["posts"]:
        likes = get_db().cursor().execute(''' SELECT * FROM likes
                                          WHERE postid=?''',
                                          (i["postid"],)).fetchall()
        i["likes"] = []
        i["did_like"] = False
        for j in likes:
            i["likes"].append(j)
            if j['owner'] == flask.session["username"]:
                i["did_like"] = True
        i["comments"] = get_db().cursor().execute(''' SELECT * FROM comments
                                                  WHERE postid=?''',
                                                  (i["postid"],)).fetchall()
    return flask.render_template("index.html", **context)


def post_ordering(post):
    """Order postid by number."""
    return post["postid"]
