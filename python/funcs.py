from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from youtube_search import YoutubeSearch
import yt_dlp

app = Flask(__name__)
CORS(app)

client_id="8ecad3e814e64a80861d1b09aaeb59ed"
client_secret="1acef6001eb64d1980d1749c71005977"
print(client_secret)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))

def get_id(artistName: str):
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

@app.route("/<artist>")
def get_album(artist):
    """This function retrieves songs from an album"""
    ID = get_id(artist)
    results = sp.artist_albums(ID, album_type='album')
    albums = results['items']
    i = 0
    for x in albums:
        tracks = sp.album_tracks(x['id'])
        albums[i]['tracks'] = tracks
        i += 1
    return jsonify(albums)


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

@cross_origin
@app.route("/download/<artist>/<song>")
def download_song(artist: str, song: str):
    results = YoutubeSearch(f"{artist} - {song} official", max_results=1).to_dict()
    print(results[0]['url_suffix'])
    best_url = f"https://www.youtube.com/{results[0]['url_suffix']}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        "quiet":    True,
        "simulate": True,
        "forceurl": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        url = ydl.extract_info(best_url)
        response = jsonify(url["url"])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=3001)