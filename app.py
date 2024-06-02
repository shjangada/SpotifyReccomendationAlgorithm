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
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-top-read,user-follow-read')

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    # clear_files()
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
    """
    items_1 = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
    top_track_uris_1 = [track['uri'] for track in items_1['items']]

    items_2 = sp.current_user_top_tracks(limit=50, offset=50, time_range='medium_term')
    top_track_uris_2 = [track['uri'] for track in items_2['items']]

    top_track_uris = top_track_uris_1 + top_track_uris_2
    
    populateCSV(top_track_uris, token_info, 'data/trackdata.csv')

    getArtists(token_info)
    """

    neutral_songs = sp.current_user_top_tracks(limit=50, offset=100, time_range='medium_term')
    time.sleep(10)
    
    populateCSV(neutral_songs, token_info, 'data/neutral.csv')
    time.sleep(10)

    create_song_database(token_info)
    
    #return str(top_track_uris)


def populateCSV(tracks, token_info, filename):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    audio_features = sp.audio_features(tracks)
    
    if audio_features is not None:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(audio_features[0].keys())
            for features in audio_features:
                writer.writerow(features.values())
    else:
        print("No audio features retrieved for the given tracks.")


def getArtists(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    followed_artists = sp.current_user_followed_artists(limit=20)['artists']['items']
    top_artists = sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')['items']
    all_artists = followed_artists + top_artists
    
    top_artist_names = [artist['name'] for artist in all_artists]
    with open('data/artists.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for artist_name in top_artist_names:
            writer.writerow([artist_name])
    
    with open('data/genres.csv', mode='a', newline='') as file:
        genres_set = set()
        writer = csv.writer(file)
        for artist in all_artists:
            genres_set.update(artist['genres']) 
        for genre in genres_set:
            writer.writerow([genre])


def create_song_database(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    with open('data/artists.csv', mode='r') as file:
        reader = csv.reader(file)
        artist_names = [row[0] for row in reader]
    
    with open('data/genres.csv', mode='r') as file:
        reader = csv.reader(file)
        genres = [row[0] for row in reader]
    
    for artist in artist_names:
        result = sp.search(q=f'artist:"{artist}"', type='track', limit=50)
        time.sleep(10)
        for tracks in result['tracks']['items']: 
            if 'id' in tracks and (tracks['popularity'] < 80):
                # Add the track ID to the list
                populateCSV(tracks['id'], token_info, 'data/songdatabase.csv')

    genre_tracks = []
    for genre in genres:
        result = sp.search(q=f'genre:"{genre}"', type='track', limit=50)
        time.sleep(10)
        for tracks in result['tracks']['items']:
            if 'id' in tracks and (tracks['popularity'] < 80):
                genre_tracks.append(tracks['id'])
    
    populateCSV(genre_tracks, token_info, 'data/songdatabase.csv')



if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(debug=True)
