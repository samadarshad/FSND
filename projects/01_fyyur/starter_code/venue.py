from flask import Blueprint, Flask, render_template, request, Response, flash, redirect, url_for
from util import *
from models import Venue, Show

venue_api = Blueprint('venue_api', __name__)

@venue_api.route('/test')
def venuetest():
    return "hello venue"

def groupVenuesByCityAndState():
  return groupClassBy(Venue, 'venues', 'city', 'state')

@venue_api.route('/')
def venues():
  data = groupVenuesByCityAndState()
  return render_template('pages/venues.html', areas=data);

@venue_api.route('/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  upcoming_shows= venue.shows.filter(Show.isUpcoming).all()
  past_shows= venue.shows.filter(Show.isUpcoming == False).all()
  return render_template('pages/show_venue.html', venue=venue,
    upcoming_shows=upcoming_shows,
    past_shows=past_shows)