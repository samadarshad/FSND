from flask import Blueprint, render_template, request, flash, redirect, url_for
from util import *
from models import Venue, Show, db
from forms import VenueForm
import sys

venue_api = Blueprint('venue_api', __name__)

#----------------------------------------------------------------------------#
# READ
#----------------------------------------------------------------------------#

def groupVenuesByCityAndState():
  return groupClassBy(db, Venue, 'venues', 'city', 'state')

@venue_api.route('/')
def venues():
  data = groupVenuesByCityAndState()
  return render_template('pages/venues.html', areas=data);

@venue_api.route('/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  upcoming_shows= venue.shows.filter(Show.isUpcoming).all()
  past_shows= venue.shows.filter(Show.isUpcoming == False).all()
  return render_template('pages/show_venue.html', venue=venue,
    upcoming_shows=upcoming_shows,
    past_shows=past_shows)

#----------------------------------------------------------------------------#
# CREATE
#----------------------------------------------------------------------------#

@venue_api.route('/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@venue_api.route('/create', methods=['POST'])
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

@venue_api.route('/search', methods=['POST'])
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

#----------------------------------------------------------------------------#
# UPDATE
#----------------------------------------------------------------------------#

@venue_api.route('/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id) 
  setFormDefaultValues(form, venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@venue_api.route('/<int:venue_id>/edit', methods=['POST'])
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
  return redirect(url_for('venue_api.show_venue', venue_id=venue_id))

#----------------------------------------------------------------------------#
# DELETE
#----------------------------------------------------------------------------#
@venue_api.route('/home')
def home_test():  
  return redirect(url_for('index'))

@venue_api.route('/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):  
  error = False
  venue = None
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
    # abort(400)
  if not error:
    flash('Venue ' + venue.name + ' was successfully deleted!')
    return redirect(url_for('index'))
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # return None

