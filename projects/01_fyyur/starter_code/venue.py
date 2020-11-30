from flask import Blueprint, render_template, request, flash, redirect, url_for
from util import *
from models import Venue, Show, db
from forms import VenueForm
import sys
from sqlalchemy import or_
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
    form = VenueForm(request.form)
    venue = populateObjectFromForm(venue, form)
    venue.creation_date = datetime.today()
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return redirect(url_for('index'))

@venue_api.route('/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term')
  terms = splitSearchTerm(search_term)
  responseByName = Venue.query.filter(or_(*[Venue.name.ilike('%' + term + '%') for term in terms])).all()
  responseByCityState = Venue.query.filter(or_(*[Venue.city.ilike('%' + term + '%') for term in terms],
                                                *[Venue.state.ilike('%' + term + '%') for term in terms])).all()
  return render_template('pages/search_venues.html', 
  resultsByName=responseByName, 
  resultsByCityState=responseByCityState, 
  search_term=request.form.get('search_term', ''))

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
  if not error:
    flash('Venue ' + venue.name + ' was successfully deleted!')
  return redirect(url_for('index'))

