from flask import Flask, request, redirect, session, url_for
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time
import spotipy
import csv
import os

app = Flask(__name__)
app.secret_key = "app!!!!"
app.config['SESSION_COOKIE_NAME'] = 'Shreyas Cookie'
TOKEN_INFO = "token_info"

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
    load_dotenv()
    return SpotifyOAuth(
        client_id = os.getenv("CLIENT_ID"),
        client_secret = os.getenv("CLIENT_SECRET"),
        redirect_uri = url_for('redirectPage', _external=True),
        scope='user-top-read,user-follow-read')

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    #clear_files()
    return redirect(auth_url)

def clear_files():
    files_to_clear = ['data/trackdata.csv', 'data/artists.csv', 'data/genres.csv', 'data/songdatabase.csv']
    for file_path in files_to_clear:
        with open(file_path, 'w') as file:
            file.write('')

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
    except:
        print("User not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Get top 100 tracks
    items_1 = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
    top_track_uris_1 = [track['uri'] for track in items_1['items']]

    items_2 = sp.current_user_top_tracks(limit=50, offset=50, time_range='medium_term')
    top_track_uris_2 = [track['uri'] for track in items_2['items']]

    # Combine the URIs from both calls
    top_track_uris = top_track_uris_1 + top_track_uris_2
    
    populateCSV(top_track_uris, token_info, 'data/trackdata.csv')
    getArtists(token_info)
    create_song_database(token_info)
    
    return str(top_track_uris)

def populateCSV(tracks, token_info, filename):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    audio_features = sp.audio_features(tracks)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(audio_features[0].keys())
        for features in audio_features:
            writer.writerow(features.values())


def getArtists(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    items = sp.current_user_followed_artists(limit=20, after=None)
    items += sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')
    top_artist_names = [artist['name'] for artist in items['artists']['items']]
    with open('data/artists.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for artist_name in top_artist_names:
            writer.writerow([artist_name])
    with open('data/genres.csv', mode='a', newline='') as file:
        genres_set = set()  # Create a set to store unique genres
        writer = csv.writer(file)
        for artist in items['artists']['items']:
            genres_set.update(artist['genres'])  # Add genres to the set to ensure uniqueness
        for genre in genres_set:
            writer.writerow([genre])  # Write each unique genre to the CSV file on a new line

def create_song_database(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    with open('data/artists.csv', mode='r') as file:
        reader = csv.reader(file)
        artist_names = [row[0] for row in reader]
    
    with open('data/genres.csv', mode='r') as file:
        reader = csv.reader(file)
        genres = [row[0] for row in reader]
    
    # Search for tracks by multiple artists
    artist_results = sp.search(q=' '.join(f'artist:"{artist}"' for artist in artist_names), type='track', limit=50)
    artist_tracks = [track['id'] for item in artist_results['tracks']['items'] for track in item]
    populateCSV(artist_tracks, token_info, 'data/songdatabase.csv')
    
    # Search for tracks by multiple genres
    genre_results = sp.search(q=' '.join(f'genre:"{genre}"' for genre in genres), type='track', limit=50)
    genre_tracks = [track['id'] for item in genre_results['tracks']['items'] for track in item]
    populateCSV(genre_tracks, token_info, 'data/songdatabase.csv')

if __name__ == '__main__':
    app.run(debug=True)
