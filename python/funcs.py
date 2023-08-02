from flask import Flask, request, jsonify
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from youtube_search import YoutubeSearch
import yt_dlp

app = Flask(__name__)

client_id="8ecad3e814e64a80861d1b09aaeb59ed"
client_secret="1acef6001eb64d1980d1749c71005977"
print(client_secret)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))

def get_artist_id(artistName: str):
    """This function retrieves artist's ID"""
    searchID = sp.search(q='artist:' + artistName, type='artist')
    ID = searchID['artists']['items'][0]['id']
    return ID

# @app.route("/<artist>")
# def get_artist_id(artist):
#     searchID = sp.search(q='artist:' + artist, type='artist')
#     ID = searchID['artists']['items'][0]['id']
#     if ID:
#         return jsonify(ID), 200

@app.route("/Albums/<artist>/<album>")
def get_album(artist, album):
    """This function retrieves songs from an album"""
    ID = get_artist_id(artist)
    results = sp.artist_albums(ID, album_type='album')
    albums = results['items']
    for x in albums:
        if x['name'] == album:
            tracks = sp.album_tracks(x['id'])
            return jsonify(tracks)
            # for track in tracks['items']:
            #     return jsonify(track)


@app.route("/Songs/<artist>/<song>")
def get_song(artist, song):
    """This function retrieves a song"""
    q = f"artist:{artist} track:{song}"
    results = sp.search(q=q, type='track')
    tracks = results['tracks']['items']
    return jsonify(tracks)
    # print(tracks)
    # for track in tracks:
    #     print(track['artists'][0]['name'] + ' - ' + track['name'])

def download_song(artist: str, song: str):
    results = YoutubeSearch(f"{artist} - {song}", max_results=1).to_dict()
    print(results[0]['url_suffix'])
    best_url = f"https://www.youtube.com/{results[0]['url_suffix']}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([best_url])


if __name__ == "__main__":
    app.run(debug=True)