from flask import render_template, flash, redirect
from application import app
from application.forms import LoginForm
from application.recommendations import Recommendation
from markupsafe import Markup, escape

@app.route('/', methods=['GET', 'POST'])
def lookup():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/recommendations/' + form.artist.data + '/' +  form.title.data)
    return render_template('lookup.html', title='Smarter Music Recommendations', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About Groover')

@app.route('/recommendations/<artist>/<title>')
def recommendations(artist, title):
    rec = Recommendation(artist, title)
    if rec.find_track_info():
        flash('{}'.format(rec.get_song_title()), category='reqtitle')

        flash('by {}'.format(
            rec.get_artist()), category='reqartist')

        message = Markup("<img src='{url}' class='centered-and-cropped' style='width:230px; height:230px;' />"
            .format(url=rec.get_album_image_url()))
        flash(message, category='reqart')

        message = Markup("<audio controls class='req' src='{url}' />"
            .format(url=rec.get_preview_url()))
        flash(message, category='reqpreview')

        rec.load_recommendations()
        for song in rec.get_recommendations():
            if((song['name'] == rec.get_song_title() and song['artist']== rec.get_artist())==False):
                flash('{}'.format(song['name']), category='songtitle')

                flash('by {}'.format(song['artist']), category='songartist')

                message = Markup("<img src='{url}' class='centered-and-cropped' style='width:215px;height:215px;' hspace='7'/>"
                    .format(url=song['image_url']))
                flash(message, category='art')

                if song['track_on_spotify'] == True and song['preview_url'] != None:
                    message = Markup("<audio controls class='rec' src='{url}' />"
                        .format(url=song['preview_url']))
                    flash(message, category='preview')

    else:
        flash('Whoops, we did not find the track "{}" by {}!'.format(
            title, artist), category='error')
        return render_template('whoops.html', title='Song Not Found')

    return render_template('recommendations.html', title='Your Recommendations')
