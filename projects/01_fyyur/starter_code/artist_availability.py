from flask import Blueprint, render_template, request, flash, redirect, url_for
from util import *
from models import ArtistAvailability, db
from forms import ArtistAvailabilityForm
import sys

artist_availability_api = Blueprint('artist_availability_api', __name__)

#----------------------------------------------------------------------------#
# CREATE
#----------------------------------------------------------------------------#

@artist_availability_api.route('/create', methods=['GET'])
def create_artist_form():
  form = ArtistAvailabilityForm()
  return render_template('forms/new_artist_availibility.html', form=form)

@artist_availability_api.route('/create', methods=['POST'])
def create_artist_submission():
  try:
    aa = ArtistAvailability()
    aa = populateObjectFromRequest(aa, request)
    db.session.add(aa)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

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