import spotify_api 
from requests import get
import json 


def search_artist(token, artist_name):
    base_url = "https://api.spotify.com/v1/search"
    headers = spotify_api.get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = base_url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists.")
        return None
    return json_result[0]

def artist_songs(token, artist_id):
    base_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = spotify_api.get_auth_header(token)
    result = get(base_url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = spotify_api.get_token()
result = search_artist(token, "Harry Styles")
artist_id = result["id"]
songs = artist_songs(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx+1}. {song['name']}")