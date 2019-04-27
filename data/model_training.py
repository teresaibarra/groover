"""This script is used to generate a model for lyrically similar songs"""

# NOTE: This code is how we generated our model and is not used actively in our
# web application -- we load the saved model in the app.

# Import all the dependencies
import csv
import json

import spotipy
from spotipy.oauth2 import SPOTIFYClientCredentials

import requests

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

# Store a list of dictionaries in SONG_DATA, then store it in a json file
SONG_DATA = []
SP_TRACKS_NOT_FOUND = 0
SP_IMAGE_NOT_FOUND = 1
SP_ARTISTS_NOT_FOUND = []
COUNTER = 0

CLIENT_CREDENTIALS_MANAGER = (SPOTIFYClientCredentials(client_id='SPOTIFY_CLIENT_ID',
                                                       client_secret='SPOTIFY_CLIENT_SECRET'))
SPOTIFY = spotipy.SPOTIFY(CLIENT_CREDENTIALS_MANAGER=CLIENT_CREDENTIALS_MANAGER)

with open('songdata.csv') as csv_file:
    CSV_READER = csv.reader(csv_file, delimiter=',')
    LINE_COUNT = 0
    for row in CSV_READER:
        if LINE_COUNT != 0:
            results = SPOTIFY.search(q='track:' + row[1] + ' artist:' + row[0], type='track')
            if len(results['tracks']['items']) > 0:
                track = results['tracks']['items'][0]
                artist_results = SPOTIFY.search(q='artist:' + row[0], type='artist')

                song_dict = {
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'lyrics': row[3].replace('\n', ' ').replace('   ', '  '),
                    'track_on_SPOTIFY': True,
                    'artist_id': track['artists'][0]['id'],
                    'genres': artist_results['artists']['items'][0]['genres'],
                    'image_url': None,

                    'preview_url': track['preview_url'],
                    'SPOTIFY_id': track['id']
                }

                if len(track['album']['images']) > 0:
                    song_dict['image_url'] = track['album']['images'][0]['url']

                SONG_DATA.append(song_dict)

            else:
                results = SPOTIFY.search(q='artist:' + row[0], type='artist')
                if len(results['artists']['items']) > 0:
                    SP_TRACKS_NOT_FOUND = SP_TRACKS_NOT_FOUND + 1

                    song_dict = {
                        'name': row[1],
                        'artist': results['artists']['items'][0]['name'],
                        'lyrics':row[3].replace('\n', ' ').replace('   ', '  '),
                        'track_on_SPOTIFY': False,
                        'artist_id': results['artists']['items'][0]['id'],
                        'genres': results['artists']['items'][0]['genres'],
                        'image_url': None
                    }

                    if len(results['artists']['items'][0]['images']) > 0:
                        SP_IMAGE_NOT_FOUND = SP_IMAGE_NOT_FOUND + 1
                        song_dict['image_url'] = results['artists']['items'][0]['images'][0]['url']

                    SONG_DATA.append(song_dict)

                else:
                    print(row)

            COUNTER = COUNTER + 1
            if COUNTER % 100 == 0:
                print("\rReading documents: %d" % COUNTER, end='', flush=True)
        LINE_COUNT += 1

JS = json.dumps(SONG_DATA)
FP = open('SONG_DATA.json', 'a') #open new json file. If it does not exist, it will create one
FP.write(JS) #write to json file
FP.close() #close the connection

with open('data/SONG_DATA.json') as json_file:
    SONG_DATA = json.load(json_file)
    SONG_LYRICS = []

    for item in SONG_DATA:
        SONG_LYRICS.append(item['lyrics'])

    TAGGED_DATA = [TaggedDocument(words=word_tokenize(_d.lower()),
                                  tags=[str(i)]) for i, _d in enumerate(SONG_LYRICS)]

    MAX_EPOCHS = 50
    VEC_SIZE = 20
    ALPHA = 0.025

    MODEL = Doc2Vec(size=VEC_SIZE,
                    alpha=ALPHA,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1)

    MODEL.build_vocab(TAGGED_DATA)

    #Train model
    for epoch in range(MAX_EPOCHS):
        print('iteration {0}'.format(epoch))
        MODEL.train(TAGGED_DATA,
                    total_examples=MODEL.corpus_count,
                    epochs=MODEL.iter)
        MODEL.ALPHA -= 0.0002 #decrease the learning rate
        MODEL.min_alpha = MODEL.ALPHA #fix the learning rate, no decay

    MODEL.save("d2v.model")
    print("Model Saved")

    #from gensim.models.doc2vec import Doc2Vec
    MODEL = Doc2Vec.load("d2v.model")

    #Use to find the vector of a document which is not in training data
    TEST_DATA = word_tokenize("hello".lower())
    V1 = MODEL.infer_vector(doc_words=TEST_DATA, alpha=0.025, min_alpha=0.001, steps=55)
    SIMILAR_V1 = MODEL.docvecs.most_similar(positive=[V1])

    for song in SIMILAR_V1:
        print(SONG_DATA[int(song[0])]['name'])
        print(SONG_DATA[int(song[0])]['artist'])
