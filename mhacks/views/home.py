"""
mhacks Create View.

URLs include:
/accounts/create/
"""
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.accountfunctions import hash_function
from mhacks.views.create_playlist import create_playlist
import requests
import spotipy
import spotipy.util as util
import google.oauth2.credentials
import google_auth_oauthlib.flow


@mhacks.app.route('/home/', methods=['GET', 'POST'])
def home():
    if 'username' not in flask.session: 
        return flask.redirect(flask.url_for('login'))
    if flask.request.method == 'POST':
    	playlistid = flask.request.form['convert-playlist'];
    	to_platform = ' ';
    	if flask.request.form['convert-to-playlist'] == "convert-to-spotify":
    		to_platform = 's'
    	elif flask.request.form['convert-to-playlist'] == "convert-to-youtube":
    		to_platform = 'y'

    	table = get_db().cursor().execute(''' SELECT * FROM playlists
                                      WHERE username=? AND id=?''',
                                      (input_username, playlistid,)).fetchone()
    	initial_platform = table['platform']
    	create_playlist(flask.session['username'], playlistid, initial_platform, to_platform)

    
    context = {}
    return flask.render_template("createPlaylist.html", **context)