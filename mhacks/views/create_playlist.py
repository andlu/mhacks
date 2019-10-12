"""
mhacks Create View.

URLs include:
/accounts/create/
"""
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.accountfunctions import file_upload, hash_function


@mhacks.app.route('/accounts/create/', methods=['GET', 'POST'])
def create_playlist(username, id_requested, initial_platform, destination_platform):
    if 'username' not in flask.session: 
        return flask.redirect(flask.url_for('login'))

    # grab playlist from the requested username, id, initial platform and destination platform 
    playlist = get_db().cursor().execute('''SELECT * FROM posts
                                        WHERE username=? AND id=? AND platform=?''', 
                                        (username,id_requested,initial_platform,)).fetchone()
        
    if (destination_platform == 's'):
        spotify_playlist(initial_platform, id_requested)
    else if (destination_platform == 'a'):
        apple_playlist(initial_platform, id_requested)
    else if (destination_platform == 'g'): 
        google_playlist(initial_platform, id_requested)
    else:  
        youtube_playlist(initial_platform, id_requested)


# grab data from initial_platform to create playlist in destination platform 
def spotify_playlist(initial_platform, id_requested): 
    GET https://api.spotify.com/v1/playlists/{playlist_id}/tracks
    curl -X GET "https://api.spotify.com/v1/playlists/{id_requested}/tracks" -H "Authorization: Bearer {access_token}"


def apple_playlist(initial_platform, id_requested): 


def google_playlist(initial_platform, id_requested): 


def youtube_playlist(initial_platform, id_requested): 