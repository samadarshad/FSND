from flask import Blueprint, Flask, render_template, request, Response, flash, redirect, url_for
from util import *
from models import Artist, Show, db
from forms import ArtistForm

artist_api = Blueprint('artist_api', __name__)


@artist_api.route('/')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@artist_api.route('/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@artist_api.route('/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  upcoming_shows= artist.shows.filter(Show.isUpcoming).all()
  past_shows= artist.shows.filter(Show.isUpcoming == False).all()
  return render_template('pages/show_artist.html', artist=artist, 
    upcoming_shows=upcoming_shows,
    past_shows=past_shows)

#  Update
#  ----------------------------------------------------------------


@artist_api.route('/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm() 
  artist = Artist.query.get(artist_id) 
  setFormDefaultValues(form, artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@artist_api.route('/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    artist = populateObjectFromRequest(artist, request)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully edited!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@artist_api.route('/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@artist_api.route('/create', methods=['POST'])
def create_artist_submission():
  try:
    artist = Artist()
    artist = populateObjectFromRequest(artist, request)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')