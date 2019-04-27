# Groover 🎵

## About
Groover is an application that neurally generates music recommendations based on a song's lyrics. This was built by [Teresa Ibarra](https://github.com/teresaibarra), [Siena Guerrero](https://github.com/sienaguerrero), [Jocelyn Chen](https://github.com/jocelynyhc), [Trevor Walker](https://github.com/trevor-walker32), and [Walker Quinn](https://github.com/wsquinn) for Harvey Mudd's [Software Development](https://www.cs.hmc.edu/program/course-descriptions/) course. See it running live [here](http://www.groovermusic.net).


## Running Locally
To run this locally, first `cd` into your project directory. Install flask_wtf using `pip install flask_wtf`, then run `virtualenv venv`. You only need to perform these previous steps once per install. 

To activate and setup the virtual environment, run `source venv/bin/activate` and `pip install -r requirements.txt`. Create a blank `.env` file.

You should set your environment variables and API keys in `.env`. `.env` should include 'FLASK_APP = groover.py', and you will need API keys for MUSIX_API_KEY, SPOTIFY_CLIENT_ID, and SPOTIFY_CLIENT_SECRET. 

When you're ready, run `flask run`.

Go to your browser and enter the address `http://127.0.0.1:5000/`.


## Issues
Follow GitHub's instructions for starting an issue for a bug (or feature request) [here](https://help.github.com/en/articles/creating-an-issue). 
