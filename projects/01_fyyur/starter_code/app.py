#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from operator import mul
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.expression import cast
from forms import *
import inspect
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db, compare_type=True)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Show', backref='venue', lazy='dynamic')

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Show', backref='artist', lazy='dynamic')

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  
  @hybrid_property
  def isUpcoming(self):
    now = datetime.now(self.start_time.tzinfo)
    return (self.start_time > now)

  @isUpcoming.expression
  def isUpcoming(cls):
    now = datetime.now()
    return (cls.start_time > now)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):  
  date = None
  if type(value) is str:
    date = dateutil.parser.parse(value)
  elif type(value) is datetime:
    date = value
  else:
    return "Error: invalid input to format_datetime"

  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
# e.g. groupClassBy(Venue, 'venues', 'city', 'state')
def groupClassBy(dbClass, dbClassDictKeyName, *argv):
  listOfAttributes = []
  for arg in argv:
    listOfAttributes.append(getattr(dbClass, arg))
  groupedClass = db.session.query(*listOfAttributes).group_by(*listOfAttributes).all()

  groupedClassDict = []

  for vals in groupedClass:
    keyvalues = {}
    for arg, val in zip(argv, vals):
      keyvalues[arg] = val
    groupedClassDict.append(keyvalues)
  
  groupedClassDict_withClass = []  

  for r in groupedClassDict:
    filterings = [(attr==r[arg]) for attr, arg in zip(listOfAttributes, argv)]
    selectedvenues = dbClass.query.filter(*filterings).all()
    groupedClassDict_withClass.append({**r, **{dbClassDictKeyName: selectedvenues}})

  return groupedClassDict_withClass

def groupVenuesByCityAndState():
  return groupClassBy(Venue, 'venues', 'city', 'state')

@app.route('/venues')
def venues():
  data = groupVenuesByCityAndState()
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  upcoming_shows= venue.shows.filter(Show.isUpcoming).all()
  past_shows= venue.shows.filter(Show.isUpcoming == False).all()
  return render_template('pages/show_venue.html', venue=venue,
    upcoming_shows=upcoming_shows,
    past_shows=past_shows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

def populateClassObject(className, request):
  obj = className()
  attributes = inspect.getmembers(className, lambda a:not(inspect.isroutine(a)))
  attributes = [a[0] for a in attributes if not(a[0].startswith('_'))]
  for a in attributes:
    if a in request.form:
      if isinstance(getattr(className, a).type, db.ARRAY):
        setattr(obj, a, request.form.getlist(a))
      else:
        setattr(obj, a, request.form[a])
  return obj

def populateObjectFromRequest(obj, request):
  attributes = inspect.getmembers(obj, lambda a:not(inspect.isroutine(a)))
  attributes = [a[0] for a in attributes if not(a[0].startswith('_'))]
  for a in attributes:
    if a in request.form:
      if isinstance(getattr(type(obj), a).type, db.ARRAY):
        setattr(obj, a, request.form.getlist(a))
      else:
        setattr(obj, a, request.form[a])
  return obj

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    venue = Venue()
    venue = populateObjectFromRequest(venue, request)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
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

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  upcoming_shows= artist.shows.filter(Show.isUpcoming).all()
  past_shows= artist.shows.filter(Show.isUpcoming == False).all()
  return render_template('pages/show_artist.html', artist=artist, 
    upcoming_shows=upcoming_shows,
    past_shows=past_shows)

#  Update
#  ----------------------------------------------------------------
def setFormDefaultValues(form, obj):
  attributes = inspect.getmembers(form, lambda a:not(inspect.isroutine(a)))
  attributes = [a[0] for a in attributes if not(a[0].startswith('_'))]
  for a in attributes:
    if hasattr(obj, a):
      setattr(getattr(form, a), "default", getattr(obj, a))
  form.process()

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm() 
  artist = Artist.query.get(artist_id) 
  setFormDefaultValues(form, artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
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

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id) 
  setFormDefaultValues(form, venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    venue = populateObjectFromRequest(venue, request)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully edited!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
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


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data=Show.query.all() 
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    show = Show()
    show = populateObjectFromRequest(show, request)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
