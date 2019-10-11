"""
mhacks Photo View.

URLs include:
/uploads/<filename>
"""
import flask
import mhacks


@mhacks.app.route('/uploads/<filename>')
def show_image(filename):
    """Send picture to user."""
    if 'username' not in flask.session:
        return flask.abort(403)
    return flask.send_from_directory(mhacks.app.config["UPLOAD_FOLDER"],
                                     filename=filename, as_attachment=True)
