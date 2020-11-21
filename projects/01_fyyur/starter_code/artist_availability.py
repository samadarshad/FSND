from datetime import datetime, timedelta
from dateutil import parser
from flask import Blueprint, render_template, request, flash, redirect, url_for
from util import *
from models import Artist, ArtistAvailability, db
from forms import ArtistAvailabilityForm
import sys

artist_availability_api = Blueprint('artist_availability_api', __name__)

#----------------------------------------------------------------------------#
# CREATE
#----------------------------------------------------------------------------#

@artist_availability_api.route('/<artist_id>/availability', methods=['GET'])
def create_artist_form(artist_id):
  form = ArtistAvailabilityForm()
  artist = Artist.query.get(artist_id)
  return render_template('forms/new_availability.html', artist=artist, form=form)

@artist_availability_api.route('/<artist_id>/availability', methods=['POST'])
def create_artist_submission(artist_id):
  try:
    aa = ArtistAvailability()
    aa.artist_id = artist_id
    aa = populateObjectFromRequest(aa, request)
    if (aa.end_time == ''):
      print("Info: No end time submitted - adding 4 hours by default")
      aa.end_time = dateutil.parser.parse(aa.start_time) + timedelta(hours=4)
      print("end time: ", aa.end_time)
    db.session.add(aa)
    db.session.commit()
    flash('Artist ' + Artist.query.get(artist_id).name + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + Artist.query.get(artist_id).name + ' could not be listed.')
  finally:
    db.session.close()
  return redirect(url_for('artist_api.show_artist', artist_id=artist_id))

#----------------------------------------------------------------------------#
# DELETE
#----------------------------------------------------------------------------#

@artist_availability_api.route('/<artist_id>', methods=['DELETE'])
def delete_artist_availabiltiy(id):
  print("deleting availability")
  error = False
  aa = None
  try:
    aa = ArtistAvailability.query.get(id)
    db.session.delete(aa)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist Availibility ' + aa.id + ' could not be deleted.')
  if not error:
    flash('Artist Availibility ' + aa.id + ' was successfully deleted!')
  return redirect(url_for('index'))