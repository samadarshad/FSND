from flask import Blueprint, Flask, render_template, request, Response, flash, redirect, url_for
from util import *
from models import Show, db
from forms import ShowForm

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

@show_api.route('/create', methods=['POST'])
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