"""
mhacks Create View.

URLs include:
/accounts/create/
"""
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.accountfunctions import file_upload, hash_function
import spotipy
# change after authorizing web app to spotify 
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

@mhacks.app.route('/accounts/create/', methods=['GET', 'POST'])
def create_playlist(username, id_requested, initial_platform, destination_platform):
    if 'username' not in flask.session: 
        return flask.redirect(flask.url_for('login'))

    # grab playlist from the requested username, id, initial platform and destination platform 
    playlist = get_db().cursor().execute('''SELECT * FROM playlists
                                        WHERE username=? AND id=? AND platform=?''', 
                                        (username,id_requested,initial_platform,)).fetchone()

    platformUsername = playlist['platformUsername'] 
    ourPlaylistID = playlist['playlistID']
    platformPlayListID = playlist['id']
    playlistTitle = playlist['title']

    if (destination_platform == 's'):
        scope = "playlist-modify-private"
        token = util.prompt_for_user_token(platformUsername,scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        if token:
            spotify_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle)
        else:
            print "Can't get token for", username

    else if (destination_platform == 'a'):
        apple_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle)
    else if (destination_platform == 'g'): 
        google_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle)
    else:  
        youtube_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle)


# grab data from initial_platform to create playlist in destination platform 
def spotify_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle): 
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    
    tracks = get_db().cursor().execute('''SELECT * FROM playListSongs
                                        WHERE username=? AND playlistID=?''', 
                                        (platformUsername, ourPlaylistID)).fetchall()
    
    user_playlist_create(platformUsername, playlistTitle, public=False, description="")

    for i in tracks:
        songID = tracks['songID']
        song = get_db().cursor().execute('''SELECT * FROM songs
                                         WHERE songID=?''', 
                                        (songID)).fetchone()
        track = search(q=song['songname']+song['artist']+sond['album'], type='track')
        user_playlist_add_tracks(platformUsername, platformPlayListID, track, position=i)
    

def apple_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle): 


def google_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle): 


def youtube_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle): 