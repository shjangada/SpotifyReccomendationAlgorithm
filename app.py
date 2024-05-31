from flask import Flask, request, redirect, session, url_for
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import spotify_api
import time
import spotipy

app = Flask(__name__)
app.secret_key = "app!!!!"
app.config['SESSION_COOKIE_NAME'] = 'Shreyas Cookie'
TOKEN_INFO = "token_info"


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks'))


@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
        print(token_info)
    except:
        print("user not logged in")
        return redirect("/")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    items = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
    top_track_uris = [track['uri'] for track in items['items']]
    return str(top_track_uris)


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("Token not found")
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = spotify_api.client_id,
        client_secret = spotify_api.client_secret,
        redirect_uri = url_for('redirectPage', _external=True),
        scope='user-top-read')
