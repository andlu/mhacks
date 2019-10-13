"""
mhacks Create View.

URLs include:
/accounts/create/
"""
import flask
from mhacks.model import get_db
import mhacks
import spotipy
import json
import spotipy.util as util
from flask import Flask, render_template, redirect, request
import requests
import base64
import config
import oauth2
import google.oauth2.credentials
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2


SPOTIPY_CLIENT_ID='03b0cc705dd74be1a04dc7b3ae8751a5'
SPOTIPY_CLIENT_SECRET='48ff64efc61a49efb1358820d846aa0e'
SPOTIPY_REDIRECT_URI_LOCAL='localhost:5000'
SPOTIPY_SERVER_CLIENT_ID='ded977cb541c4fa8b1ff1c933e923d5f'
SPOTIPY_SERVER_CLIENT_SECRET='46a4fec7801947c8a1fb4934a916fc94'
SPOTIPY_REDIRECT_URI_SERVER='https://mhacks-255703.appspot.com/'


def read_playlist(username_in, initial_platform):
    # if 'username_in' not in flask.session: 
    #     return flask.redirect(flask.url_for('login'))

    # print ('Getting the access token')
    # post_url = 'https://accounts.spotify.com/api/token'
    # grant_type = 'authorization_code'
    # # callback_url = 'http://127.0.0.1:5000/callback'
    # callback_url = request.url_root + 'callback'
    # authorization = config.authorization

    # post = {'redirect_uri': callback_url, 'code': code, 'grant_type': grant_type}
    # headers = {'Authorization': authorization, 'Accept': 'application/json',
    #            'Content-Type': 'application/x-www-form-urlencoded'}

    # r = requests.post(post_url, headers=headers, data=post)
    # auth_json = json.loads(r.text)
    # try:
    #     access_token = 'Bearer ' + auth_json['access_token']
    #     print (access_token)
    #     return access_token
    # except Exception as e:
    #     print ("Something went wrong at the Spotify end - press back and try again")
    #     return "Something went wrong at the Spotify end - press back and try again"

    if (initial_platform == 's'):
        spotify_playlist(username_in)
    elif (initial_platform == 'y'):
        youtube_playlist(platform_id, id_requested)

# get tokens 
def spotify_playlist(input_username): 
    # if __name__ == '__main__':
    #     if len(sys.argv) > 1:
    #         username = sys.argv[1]
    #     else:
    #         print("Whoops, need your username!")
    #         print("usage: python user_playlists_contents.py [username]")
    #         sys.exit()

        username = input_username
        # change after authorizing web app to spotify 
        scope = 'playlist-read-private'

        # token = util.prompt_for_user_token(username,scope, client_id='03b0cc705dd74be1a04dc7b3ae8751a5',client_secret='48ff64efc61a49efb1358820d846aa0e',redirect_uri='http://localhost:5000/getPlaylists/')
        credentials = oauth2.SpotifyClientCredentials(client_id=SPOTIPY_SERVER_CLIENT_ID, client_secret=SPOTIPY_SERVER_CLIENT_SECRET)
        token = credentials.get_access_token()
        spotify = spotipy.Spotify(auth=token)
        fromPlatform = 'Spotify'
        if token:
            sp = spotipy.Spotify(auth=token)
            #res = requests.get("https://api.spotify.com/v1/me" -H "Authorization: Bearer {token}")
            #userID = res['id']
            #sp.trace = False
            playlists = sp.user_playlists(input_username)
            
            for playlist in playlists:
                tracks = playlist['tracks']
                for track in tracks:
                    get_db().cursor().execute(''' INSERT INTO songs 
                                                (songName, artist, album)
                                                VALUES (?, ?, ?) '''
                                                (track['name'], track['artist'][0]['name'], track['album']['name']))

                get_db().cursor().execute(''' INSERT INTO playlists 
                                            (title, id, 
                                            url, platform, platformUsername)
                                            VALUES (?, ?, ?, ?, ?, ?) '''
                                            (playlist['name'], playlist['id'],
                                            playlist['url'], fromPlatform, playlist['owner'])
                )
        else:
            print("Can't get token for", input_username)



# @mhacks.app.route('/getPlaylists/', methods=['GET', 'POST'])
# def getPlaylists():
#     token = util.prompt_for_user_token(username,scope, client_id='03b0cc705dd74be1a04dc7b3ae8751a5',client_secret='48ff64efc61a49efb1358820d846aa0e',redirect_uri='http://localhost:5000/getPlaylists/')
#     fromPlatform = 'Spotify'
#     if token:
#         sp = spotipy.Spotify(auth=token)
#         #sp.trace = False
#         playlists = sp.user_playlists(username_in_spotify)
        
#         for playlist in playlists['items']:
#             if playlist['owner']['id'] == username:
#                 #print()
#                 #print(playlist['name'])
#                 #print('  total tracks', playlist['tracks']['total'])
#                 results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
#                 tracks = results['tracks']
#                 alert("hasd")
#                 for track in tracks['next']:
#                     get_db().cursor().execute(''' INSERT INTO songs 
#                                                 (songName, artist, album)
#                                                 VALUES (?, ?, ?) '''
#                                                 (track['name'], track['artists'], track['album'])
#                     )

#                     tracks = sp.next(tracks)

#                 get_db().cursor().execute(''' INSERT INTO playlists 
#                                             (title, id, 
#                                             url, platform, platformUsername)
#                                             VALUES (?, ?, ?, ?, ?, ?) '''
#                                             (playlist['name'], playlist['id'],
#                                             playlist['url'], fromPlatform, playlist['owner'])
#                 )
#     else:
#         print("Can't get token for", username)

def youtube_playlist(platform_id, id_requested): 
    # authorization functions go here
    mhacks.app.add_url_rule('/', 'index', index)
    mhacks.app.add_url_rule('/test', 'test_api_request', test_api_request)
    mhacks.app.add_url_rule('/authorize', 'authorize', authorize)
    mhacks.app.add_url_rule('oauth2callback', 'oauth2callback', oauth2callback)
