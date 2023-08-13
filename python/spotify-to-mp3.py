import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from youtube_search import YoutubeSearch
import yt_dlp

client_id="8ecad3e814e64a80861d1b09aaeb59ed"
client_secret="1acef6001eb64d1980d1749c71005977"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))


def get_artist_id(artistName: str):
    """This function retrieves artist's ID"""
    searchID = sp.search(q='artist:' + artistName, type='artist')
    ID = searchID['artists']['items'][0]['id']
    return ID


def get_album(artist: str, album: str):
    """This function retrieves songs from an album"""
    ID = get_artist_id(artist)
    results = sp.artist_albums(ID, album_type='album')
    albums = results['items']
    for x in albums:
        if x['name'] == album:
            tracks = sp.album_tracks(x['id'])
            for track in tracks['items']:
                print(json.dumps(track))


def get_song(artist: str, song: str):
    """This function retrieves a song"""
    q = f"artist:{artist} track:{song}"
    results = sp.search(q=q, type='track')
    tracks = results['tracks']['items']
    print(tracks)
    for track in tracks:
        print(track['artists'][0]['name'] + ' - ' + track['name'])

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

download_song("Logic", "Heard Em Say")