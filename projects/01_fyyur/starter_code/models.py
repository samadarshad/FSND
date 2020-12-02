from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

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
    seeking = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Show', backref=__tablename__, lazy='dynamic')
    creation_date = db.Column(db.DateTime, nullable=False)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Show', backref=__tablename__, lazy='dynamic')    
    availability = db.relationship('ArtistAvailability', backref=__tablename__, lazy='dynamic')
    creation_date = db.Column(db.DateTime, nullable=False)

class ArtistAvailability(db.Model):
    __tablename__ = 'artist_availabilities'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime, nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  
  @hybrid_property
  def isUpcoming(self):
    now = datetime.now(self.start_time.tzinfo)
    return (self.start_time > now)

  @isUpcoming.expression
  def isUpcoming(cls):
    now = datetime.now()
    return (cls.start_time > now)
