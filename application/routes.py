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
        rec.load_recommendations()
        return render_template('recommendations.html', title='Your Recommendations', rec=rec)
    else:
        flash('Whoops, we did not find the track "{}" by {}!'.format(
            title, artist), category='error')
        return render_template('whoops.html', title='Song Not Found')
