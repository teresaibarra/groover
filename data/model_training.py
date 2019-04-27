# NOTE: This code is how we generated our model and is not used actively in our
# web application -- we load the saved model in the app.

# Import all the dependencies
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import csv
import spotipy
import requests
import json
from spotipy.oauth2 import SpotifyClientCredentials

# Store a list of dictionaries in song_data, then store it in a json file
song_data = []
sp_tracks_not_found = 0
sp_image_not_found = 1
sp_artists_not_found = []
counter = 0

client_credentials_manager = SpotifyClientCredentials(client_id='SPOTIFY_CLIENT_ID', client_secret='SPOTIFY_CLIENT_SECRET')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

with open('songdata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            results = spotify.search(q='track:' + row[1] + ' artist:' + row[0], type='track')
            if len(results['tracks']['items']) > 0:
                track = results['tracks']['items'][0]
                artist_results = spotify.search(q='artist:' + row[0], type='artist')

                song_dict = {
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'lyrics': row[3].replace('\n', ' ').replace('   ', '  '),
                    'track_on_spotify': True,
                    'artist_id': track['artists'][0]['id'],
                    'genres': artist_results['artists']['items'][0]['genres'],
                    'image_url': None,

                    'preview_url': track['preview_url'],
                    'spotify_id': track['id']
                }

                if len(track['album']['images']) > 0:
                    song_dict['image_url'] = track['album']['images'][0]['url']

                song_data.append(song_dict)

            else:
                results = spotify.search(q='artist:' + row[0], type='artist')
                if len(results['artists']['items']) > 0:
                    sp_tracks_not_found = sp_tracks_not_found + 1

                    song_dict = {
                        'name': row[1],
                        'artist': results['artists']['items'][0]['name'],
                        'lyrics':row[3].replace('\n', ' ').replace('   ', '  '),
                        'track_on_spotify': False,
                        'artist_id': results['artists']['items'][0]['id'],
                        'genres': results['artists']['items'][0]['genres'],
                        'image_url': None
                    }

                    if len(results['artists']['items'][0]['images']) > 0:
                        sp_image_not_found = sp_image_not_found + 1
                        song_dict['image_url'] = results['artists']['items'][0]['images'][0]['url']

                    song_data.append(song_dict)

                else:
                    print(row)

            counter = counter + 1
            if counter % 100 == 0:
                print("\rReading documents: %d" % counter, end='', flush=True)
        line_count += 1

js = json.dumps(song_data)
fp = open('song_data.json', 'a') #open new json file. If it does not exist, it will create one
fp.write(js) #write to json file
fp.close() #close the connection

with open('data/song_data.json') as json_file:
    song_data = json.load(json_file)
    song_lyrics = []

    for item in song_data:
        song_lyrics.append(item['lyrics'])

    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(song_lyrics)]

    max_epochs = 50
    vec_size = 20
    alpha = 0.025

    model = Doc2Vec(size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=1,
                    dm =1)

    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    model.save("d2v.model")
    print("Model Saved")

    from gensim.models.doc2vec import Doc2Vec
    model= Doc2Vec.load("d2v.model")

    #Use to find the vector of a document which is not in training data
    test_data = word_tokenize("hello".lower())
    v1 = model.infer_vector(doc_words=test_data, alpha=0.025, min_alpha=0.001, steps=55)
    similar_v1 = model.docvecs.most_similar(positive=[v1])

    for song in similar_v1:
        print(song_data[int(song[0])]['name'])
        print(song_data[int(song[0])]['artist'])
