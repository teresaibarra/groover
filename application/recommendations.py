import requests
import json
import os
import spotipy
import re

from flask import render_template, flash, redirect
from application import app
from application.forms import LoginForm
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
from markupsafe import Markup
from spotipy.oauth2 import SpotifyClientCredentials


class Recommendation:
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.track_id = None
        self.lyrics = None
        self.album_image_url = None
        self.preview_url = None
        self.recommendations = None
        self.spotify_url = None

    def get_musixmatch_api_url(self, url):
        return 'http://api.musixmatch.com/ws/1.1/{}&format=json&apikey={}'.format(url, os.getenv("MUSIX_API_KEY"))

    def find_track_info(self):
        url = 'matcher.track.get?q_track={}&q_artist={}'.format(self.get_song_title(), self.get_artist())
        matched_res = requests.get(self.get_musixmatch_api_url(url))
        matched_data = json.loads(matched_res.text)

        if matched_data["message"]["header"]["status_code"] == 200:
            # get initial musixmatch information
            self.artist = matched_data["message"]["body"]["track"]["artist_name"]
            self.title = matched_data["message"]["body"]["track"]["track_name"]
            self.track_id = matched_data["message"]["body"]["track"]["track_id"]

            # make another api call for the lyrics
            url = 'track.lyrics.get?track_id={}'.format(self.get_track_id())
            lyrical_res = requests.get(self.get_musixmatch_api_url(url))
            lyrical_data = json.loads(lyrical_res.text)
            self.lyrics = lyrical_data["message"]["body"]["lyrics"]["lyrics_body"].split("...")[0]

            # get album art and a preview url from Spotify
            client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_CLIENT_ID"), client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"))
            spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            results = spotify.search(q='track:' + self.get_song_title() + ' artist:' + self.get_artist(), type='track')
            track = results['tracks']['items'][0]
            self.album_image_url = track["album"]["images"][1]["url"]
            self.preview_url = track["preview_url"]
            self.spotify_url = track['external_urls']['spotify']

            return True
        else:
            print('Track not found.')
            return False

    def load_recommendations(self):
        lyrics = self.get_lyrics().strip().replace('\n',' ').lower()
        lyrics = re.sub("[\(\[].*?[\)\]]", "", lyrics)

        # get most similar lysics
        model = Doc2Vec.load("data/d2v.model")
        test_data = word_tokenize(lyrics)
        v1 = model.infer_vector(doc_words=test_data, alpha=0.025, min_alpha=0.001, steps=55)
        # this returns a list of tuples -- the first element of the tuple is
        # its index in the song_data list
        list_of_tuples = model.docvecs.most_similar(positive=[v1])

        recommendations = []
        with open('data/song_data.json') as json_file:
            song_data = json.load(json_file)
            for ranking_tuple in list_of_tuples:
                recommendations.append(song_data[int(ranking_tuple[0])])

        self.recommendations = recommendations
        return True

    def get_artist(self):
        return self.artist

    def get_song_title(self):
        return self.title

    def get_track_id(self):
        return self.track_id

    def get_lyrics(self):
        return self.lyrics

    def get_album_image_url(self):
        return self.album_image_url

    def get_preview_url(self):
        return self.preview_url

    def get_spotify_url(self):
        return self.spotify_url

    def get_recommendations(self):
        return self.recommendations
