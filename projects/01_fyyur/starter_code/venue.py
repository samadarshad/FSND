from flask import Blueprint, Flask, render_template, request, Response, flash, redirect, url_for
from util import *
from models import Venue

venue_api = Blueprint('venue', __name__)

@venue_api.route('/test')
def venuetest():
    return "hello venue"

def groupVenuesByCityAndState():
  return groupClassBy(Venue, 'venues', 'city', 'state')

@venue_api.route('/')
def venueshome():
  data = groupVenuesByCityAndState()
  return render_template('pages/venues.html', areas=data);