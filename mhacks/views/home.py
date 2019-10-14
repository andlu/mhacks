"""
mhacks Create View.

URLs include:
/accounts/create/
"""
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.create_playlist import create_playlist
from mhacks.views.read_playlist import read_playlist
import requests
import spotipy
import spotipy.util as util
#import google.oauth2.credentials
#import google_auth_oauthlib.flow


@mhacks.app.route('/home/', methods=['GET', 'POST'])
def home():
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
        
    input_username = flask.session['username']
    if flask.request.method == 'POST':
        if 'Spotify' in flask.request.form:
            username_in = flask.request.form['Spotify Username']
            read_playlist(username_in, 's')
            return flask.redirect(flask.url_for('home'))
        elif 'Youtube' in flask.request.form:
            read_playlist(flask.session['username'], 'y')
            return flask.redirect(flask.url_for('home'))
        else:
            playlistid = -1
            to_platform = ' '
            if 'Convert to Spotify' in flask.request.form:
                playlistid = flask.request.form['Convert to Spotify']
                to_platform = 's'
            else:
                playlistid = flask.request.form['Convert to Youtube']
                to_platform = 'y'

            table = get_db().cursor().execute(''' SELECT * FROM playlists
                                    WHERE username=? AND id=?''',
                                    (flask.session['username'], playlistid,)).fetchone()
            initial_platform = table['platform']
            create_playlist(flask.session['username'], playlistid, initial_platform, to_platform)

    playlists = get_db().cursor().execute(''' SELECT * FROM playlists
                                    WHERE username=?''',
                                    (flask.session['username'],)).fetchall()
    context = {}
    context['playlists'] = []
    for playlist in playlists:
        temp = {}
        temp['playlistID'] = playlist['playlistID']
        temp['title'] = playlist['title']

        songs = get_db().cursor().execute(''' SELECT * FROM playListSongs
                                    WHERE username=? AND databasePlaylistID=?''',
                                    (flask.session['username'], playlist['playlistID'],)).fetchall()
        temp['playlistID'] = playlist['playlistID']
        songTemp = []
        for song in songs:
            specific_song = get_db().cursor().execute(''' SELECT * FROM songs
                                    WHERE songID=? ''',
                                    (song['songID'],)).fetchone()
            songTemp2 = {}
            songTemp2['title'] = specific_song['title']
            songTemp2['artist'] = specific_song['artist']
            songTemp.append(songTemp2)

        temp['songs'] = songTemp
        context['playlists'].append(temp)

    return flask.render_template("createPlaylist.html", **context)
