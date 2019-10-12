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
import json
import spotipy.util as util

# change after authorizing web app to spotify 
SPOTIPY_CLIENT_ID='your-spotify-client-id'
SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
SPOTIPY_REDIRECT_URI='your-app-redirect-url'

@mhacks.app.route('/accounts/create/', methods=['GET', 'POST'])
def read_playlist(username_in, initial_platform):
    if 'username_in' not in flask.session: 
        return flask.redirect(flask.url_for('login'))

    if (initial_platform == 's'):
        spotify_playlist()
    elif (initial_platform == 'y'):
        youtube_playlist(platform_id, id_requested)


# grab data from initial_platform to create playlist in destination platform 
def spotify_playlist(): 
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    
    def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))

    if __name__ == '__main__':
        if len(sys.argv) > 1:
            username = sys.argv[1]
        else:
            print("Whoops, need your username!")
            print("usage: python user_playlists_contents.py [username]")
            sys.exit()

        token = util.prompt_for_user_token(username)
        fromPlatform = 'Spotify'
        if token:
            sp = spotipy.Spotify(auth=token)
            playlists = sp.user_playlists(username)
            for playlist in playlists['items']:
                if playlist['owner']['id'] == username:
                    #print()
                    #print(playlist['name'])
                    #print('  total tracks', playlist['tracks']['total'])
                    results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                    tracks = results['tracks']
                    show_tracks(tracks)
                    for track in tracks['next']:
                        tracks = sp.next(tracks)
                        show_tracks(tracks)
                        get_db().cursor().execute(''' INSERT INTO songs 
                                                    (songName, artist, album)
                                                    VALUES (?, ?, ?) '''
                                                    (track['name'], track['artists'], track['album'])
                    )

                    get_db().cursor().execute(''' INSERT INTO playlists 
                                                (title, id, 
                                                url, platform, platformUsername)
                                                VALUES (?, ?, ?, ?, ?, ?) '''
                                                (playlist['name'], playlist['id'],
                                                playlist['url'], fromPlatform, playlist['owner'])
                    )

        else:
            print("Can't get token for", username)

def youtube_playlist(platform_id, id_requested): 

