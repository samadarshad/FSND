import sys
from flask import Blueprint, render_template, request, flash, redirect, url_for
from util import *
from models import Artist, ArtistAvailability, Show, db
from forms import ShowForm
from constants import *

show_api = Blueprint('show_api', __name__)

#----------------------------------------------------------------------------#
# READ
#----------------------------------------------------------------------------#

@show_api.route('/')
def shows():
  data=Show.query.all() 
  return render_template('pages/shows.html', shows=data)

#----------------------------------------------------------------------------#
# CREATE
#----------------------------------------------------------------------------#

@show_api.route('/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

def isShowWithinArtistAvailibility(show: Show):
  availabilitiesQuery = ArtistAvailability.query.filter_by(artist_id = show.artist_id)
  if len(availabilitiesQuery.all()) == 0:
    print("Unspecified availability - artist is fully available")
    return True
  else:
    validSlot = availabilitiesQuery.filter(ArtistAvailability.start_time < show.start_time).filter(ArtistAvailability.end_time > show.end_time).all()
    if len(validSlot) == 0:
      print("Could not find a valid slot, given that show time.")
      return False
  return True

class ArtistUnavailable(Exception):
  pass

@show_api.route('/create', methods=['POST'])
def create_show_submission():
  try:
    show = Show()
    show = populateObjectFromRequest(show, request)
    if (show.end_time == ''):
      print("Info: No end time submitted - adding default")
      show.end_time = dateutil.parser.parse(show.start_time) + default_booking_slot_duration
      print("end time: ", show.end_time)
    if not isShowWithinArtistAvailibility(show):
      raise ArtistUnavailable
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except ArtistUnavailable:
    db.session.rollback()
    flash('An error occurred. Artist is not available during requested booking slot. Show could not be listed.')
  except:
    print(sys.exc_info())
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return redirect(url_for('index'))