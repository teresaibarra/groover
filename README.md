# Groover 🎵

## About
Groover is an application that neurally generates music recommendations based on a song's lyrics. This was built by [Teresa Ibarra](https://github.com/teresaibarra), [Siena Guerrero](https://github.com/sienaguerrero), [Jocelyn Chen](https://github.com/jocelynyhc), [Trevor Walker](https://github.com/trevor-walker32), and [Walker Quinn](https://github.com/wsquinn) for Harvey Mudd's [Software Development](https://www.cs.hmc.edu/program/course-descriptions/) course. See it running live [here](http://www.groovermusic.net).

## Model
Our model was built with a Gensim Doc2Vec model and its similarity ranking capabilities. Gensim is a Python library used
for topic modelling and Doc2Vec is a class within Gensim that modifies the word2vec algorithm to create a representation of
large blocks of text (or documents) in vector form. In this case, we pass in song lyrics as a document. We first train our model in Python with a database of lyrics of 57,000 songs with 50 epochs. We then infer the vector of a new input song’s lyrics, and then find vectors within our database that are the most similar. We then find the songs that correspond with the most similar vectors, resulting in a list of songs with the most similar lyrics to our input song.
There is no way to concretely test the performance of the model. However, we have found that if we query a song that is
already in our database, the same song is returned as the most similar result. This is expected because the lyrics should still be the same.

## Python Script
Our architecture uses Python scripting to communicate with Spotify and Musixmatch’s API, as well as communicating with
our document similarity model and our song database.

## JSON Files
We stored our model as a JSON because this is a static application that does not require any changes to the
database. Therefore, it was easier to store our database as a JSON file, which would then be loaded when needed.

## Web App
We found that it was easiest to deploy our application with Heroku instead of manually setting up with Amazon
Web Services. We had spent several weeks attempting to set up our server on EC2, but struggled to connect this with Github.
Heroku has automatic deployments to our website once a change was pushed to our master branch on Github, which greatly
simplified our deployment process.

## Demo
![alt text](documentation/GrooverDemo.gif "Groover Demo")


## Running Locally
To run this locally, first `cd` into your project directory. Install flask_wtf using `pip install flask_wtf`, then run `virtualenv venv`. You only need to perform these previous steps once per install. 

To activate and setup the virtual environment, run `source venv/bin/activate` and `pip install -r requirements.txt`. Create a blank `.env` file.

You should set your environment variables and API keys in `.env`. `.env` should include 'FLASK_APP = groover.py', and you will need API keys for MUSIX_API_KEY, SPOTIFY_CLIENT_ID, and SPOTIFY_CLIENT_SECRET. 

When you're ready, run `flask run`.

Go to your browser and enter the address `http://127.0.0.1:5000/`.


## Issues
Follow GitHub's instructions for starting an issue for a bug (or feature request) [here](https://help.github.com/en/articles/creating-an-issue). 
