"""
This file handles the input from routes and generates the
recommendations using the API calls to musixmatch and spotipy
"""
import json
import re
import os
import requests
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Recommendation Generator
class Recommendation:
    """
    The recommendation class will initialize the song display
    to be used on the recommendation page
    """
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.track_id = None
        self.lyrics = None
        self.album_image_url = None
        self.preview_url = None
        self.recommendations = None
        self.spotify_url = None

    # Retrieve URL for song on Musixmatch
    def get_musixmatch_api_url(self, url):
        """
        this method will build the url to grab the json from
        musixmatch, which we will use for the lyrics and song
        information. Uses the MusixMatch API key.
        """
        return 'http://api.musixmatch.com/ws/1.1/{}&format=json&apikey={}'.format(url, \
        os.getenv("MUSIX_API_KEY"))
    # Retrieve song info from Musixmatch and Spotify
    def find_track_info(self):
        """
        uses the url from get_musixmatch_api_url to load the json file into matched
        data, so we could use it later.
        """
        url = 'matcher.track.get?q_track={}&q_artist={}'.format(self.get_song_title(), \
        self.get_artist())
        matched_res = requests.get(self.get_musixmatch_api_url(url))
        matched_data = json.loads(matched_res.text)

        if matched_data["message"]["header"]["status_code"] == 200:
            #Get initial Musixmatch information
            self.artist = matched_data["message"]["body"]["track"]["artist_name"]
            self.title = matched_data["message"]["body"]["track"]["track_name"]
            self.track_id = matched_data["message"]["body"]["track"]["track_id"]

            #Make another API call for the lyrics
            url = 'track.lyrics.get?track_id={}'.format(self.get_track_id())
            lyrical_res = requests.get(self.get_musixmatch_api_url(url))
            lyrical_data = json.loads(lyrical_res.text)
            self.lyrics = lyrical_data["message"]["body"]["lyrics"]["lyrics_body"].split("...")[0]

            #Access Spotify API
            client_credentials_manager = SpotifyClientCredentials(\
            client_id=os.getenv("SPOTIFY_CLIENT_ID"), \
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"))
            spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            #Get album art and a preview url from Spotify
            results = spotify.search(q='track:' + self.get_song_title() + \
            ' artist:' + self.get_artist(), type='track')
            try:
                track = results['tracks']['items'][0]
                self.album_image_url = track["album"]["images"][1]["url"]
                self.preview_url = track["preview_url"]
                self.spotify_url = track['external_urls']['spotify']

                return True
            except:
                print('Track not found.')
                return False
        print('Track not found.')
        return False


    # Determine song recommendations using model
    def load_recommendations(self):
        """
        clean the input so it works with our model (lowercase, etc)
        use doc to vec which returns indices in the database that
        we will use to list recommendations.
        """
        #Clean lyrics for analysis
        lyrics = self.get_lyrics().strip().replace('\n', ' ').lower()
        lyrics = re.sub(r"[\(\[].*?[\)\]]", r"", lyrics)

        #Get most similar lysics
        model = Doc2Vec.load("data/d2v.model") #load model
        test_data = word_tokenize(lyrics)
        vector_1 = model.infer_vector(doc_words=test_data, alpha=0.025, \
        min_alpha=0.001, steps=55)

        list_of_tuples = model.docvecs.most_similar(positive=[vector_1],\
         topn=20)  #first element of the tuple its index in the song_data list
        recommendations = []

        #Store generated song recommendations from model
        with open('data/song_data.json') as json_file:
            song_data = json.load(json_file)
            for ranking_tuple in list_of_tuples:
                song = song_data[int(ranking_tuple[0])]
                song['genres'] = [g.title() for g in song['genres']]
                if song['name'] != self.get_song_title():
                    recommendations.append(song)

        self.recommendations = recommendations
        return True


    def get_artist(self):
        """
        helper function to return artist name
        """
        return self.artist

    def get_song_title(self):
        """
        helper function to return song name
        """
        return self.title

    def get_track_id(self):
        """
        helper function to return track id so
        we could find it using the API for
        spotify and musixmatch
        """
        return self.track_id

    def get_lyrics(self):
        """
        helper function to return 1/3 of the
        song lyrics
        """
        return self.lyrics

    def get_album_image_url(self):
        """
        helper function to return album art
        associated with song
        """
        return self.album_image_url

    def get_preview_url(self):
        """
        helper function to return preview url
        so user can see song on rec page
        """
        return self.preview_url

    def get_spotify_url(self):
        """
        helper function to return url so
        user can visit song on spotify
        """
        return self.spotify_url

    def get_recommendations(self):
        """
        helper function to return
        recommendations using our
        model
        """
        return self.recommendations
