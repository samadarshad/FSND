from flask import Blueprint, render_template, request, flash, redirect, url_for
from util import *
from models import Artist, Show, db
from forms import ArtistForm
import sys
from sqlalchemy import or_

artist_api = Blueprint('artist_api', __name__)

#----------------------------------------------------------------------------#
# READ
#----------------------------------------------------------------------------#

@artist_api.route('/')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@artist_api.route('/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term')
  terms = splitSearchTerm(search_term)
  responseByName = Artist.query.filter(or_(*[Artist.name.ilike('%' + term + '%') for term in terms])).all()
  responseByCityState = Artist.query.filter(or_(*[Artist.city.ilike('%' + term + '%') for term in terms],
                                                *[Artist.state.ilike('%' + term + '%') for term in terms])).all()
  return render_template('pages/search_artists.html', 
  resultsByName=responseByName, 
  resultsByCityState=responseByCityState, 
  search_term=request.form.get('search_term', ''))

@artist_api.route('/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  upcoming_shows= artist.shows.filter(Show.isUpcoming).all()
  past_shows= artist.shows.filter(Show.isUpcoming == False).all()
  return render_template('pages/show_artist.html', artist=artist, 
    upcoming_shows=upcoming_shows,
    past_shows=past_shows)

#----------------------------------------------------------------------------#
# CREATE
#----------------------------------------------------------------------------#

@artist_api.route('/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@artist_api.route('/create', methods=['POST'])
def create_artist_submission():
  try:
    artist = Artist()
    form = ArtistForm(request.form)
    artist = populateObjectFromForm(artist, form)
    artist.creation_date = datetime.today()
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return redirect(url_for('index'))

#----------------------------------------------------------------------------#
# UPDATE
#----------------------------------------------------------------------------#

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
    form = ArtistForm(request.form)
    artist = populateObjectFromForm(artist, form)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully edited!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
  finally:
    db.session.close()
  return redirect(url_for('artist_api.show_artist', artist_id=artist_id))

#----------------------------------------------------------------------------#
# DELETE
#----------------------------------------------------------------------------#

@artist_api.route('/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  print("deleting artist")
  error = False
  artist = None
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + artist.name + ' could not be deleted.')
  if not error:
    flash('Artist ' + artist.name + ' was successfully deleted!')
  return redirect(url_for('index'))