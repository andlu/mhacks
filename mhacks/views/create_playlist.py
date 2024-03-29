"""
"""
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.accountfunctions import hash_function
import requests
import spotipy
import spotipy.util as util
#import google.oauth2.credentials
#import google_auth_oauthlib.flow

# change after authorizing web app to spotify 
SPOTIPY_CLIENT_ID='03b0cc705dd74be1a04dc7b3ae8751a5'
SPOTIPY_CLIENT_SECRET='48ff64efc61a49efb1358820d846aa0e'
SPOTIPY_REDIRECT_URI_SERVER='https://mhacks-255703.appspot.com/'
SPOTIPY_REDIRECT_URI_LOCAL='localhost:5000'


def create_playlist(username, id_requested, initial_platform, destination_platform):
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
        token = util.prompt_for_user_token(platformUsername,scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI_LOCAL)
        if token:
            spotify_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle)
        else:
            print ("Can't get token for", username)
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


def youtube_playlist(platformUsername, ourPlaylistID, platformPlayListID, playlistTitle): 
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scope=['https://www.googleapis.com/auth/youtubepartner'])

    flow.redirect_uri = 'https://www.example.com/oauth2callback' # change redirect to actual redirect link 

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        state=sample_passthrough_value, 
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')