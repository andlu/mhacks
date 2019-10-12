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
    playlist = get_db().cursor().execute('''SELECT * FROM posts
                                        WHERE username=? AND id=? AND platform=?''', 
                                        (username,id_requested,initial_platform,)).fetchone()

    platformUsername = playlist['platformUsername'] 

    if (destination_platform == 's'):
        scope = "playlist-modify-private"
        token = util.prompt_for_user_token(platformUsername,scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        if token:
            spotify_playlist(platformUsername, id_requested)
        else:
            print "Can't get token for", username

        spotify_playlist(platform_id, id_requested)
    else if (destination_platform == 'a'):
        apple_playlist(platform_id, id_requested)
    else if (destination_platform == 'g'): 
        google_playlist(platform_id, id_requested)
    else:  
        youtube_playlist(platform_id, id_requested)


# grab data from initial_platform to create playlist in destination platform 
def spotify_playlist(platformUsername, id_requested): 
    sp = spotipy.Spotify(auth=token)
    
    tracks = get_db().cursor(), execute('''SELECT * FROM playListSongs
                                        WHERE username=? AND playlist=?''', 
                                        (platformUsername, ))
    

def apple_playlist(platform_id, id_requested): 


def google_playlist(platform_id, id_requested): 


def youtube_playlist(platform_id, id_requested): 


# JSON response to creating a new playlist
{"collaborative":false, 
"description":null,
"external_urls":{"spotify":"http://open.spotify.com/user/thelinmichael/playlist/7d2D2S200NyUE5KYs80PwO"},
"followers":{"href":null,"total":0},
"href":"https://api.spotify.com/v1/users/thelinmichael/playlists/7d2D2S200NyUE5KYs80PwO",
"id":"7d2D2S200NyUE5KYs80PwO",
"images":[],
"name":"A New Playlist",
"owner":{"external_urls":{"spotify":"http://open.spotify.com/user/thelinmichael"},
"href":"https://api.spotify.com/v1/users/thelinmichael",
"id":"thelinmichael",
"type":"user",
"uri":"spotify:user:thelinmichael"},
"public":false,
"snapshot_id":"s0o3TSuYnRLl2jch+oA4OEbKwq/fNxhGBkSPnvhZdmWjNV0q3uCAWuGIhEx8SHIx",
"tracks":{"href":"https://api.spotify.com/v1/users/thelinmichael/playlists/7d2D2S200NyUE5KYs80PwO/tracks",
"items":[],"limit":100,"next":null,"offset":0,"previous":null,"total":0},
"type":"playlist",
"uri":"spotify:user:thelinmichael:playlist:7d2D2S200NyUE5KYs80PwO"}