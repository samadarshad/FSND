#THIS ONLY WORKS ON DB VERSION 679779ce0d82, so on a new DB, do: 
# createdb fyyurdb
# flask db init
# flask db upgrade '679779ce0d82'
# python3 populate_db.py
# flask db upgrade
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
db.app = app

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
    shows = db.relationship('Show', backref='venue', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

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
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  # instead of artist_id, have the actual artist be referenced here, so you can do show.artist.id instead of show.artist_id




venue1 = Venue(
    name="The Musical Hop", 
    city="San Francisco",
    state="CA",
    address="1015 Folsom Street",    
    phone="123-123-1234",
    website="https://www.themusicalhop.com",
    image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    facebook_link="https://www.facebook.com/TheMusicalHop",
    genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    seeking_talent=True,
    seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us."
)

venue2 = Venue(
    name = "The Dueling Pianos Bar",
    genres = ["Classical", "R&B", "Hip-Hop"],
    address = "335 Delancey Street",
    city = "New York",
    state = "NY",
    phone = "914-003-1132",
    website = "https://www.theduelingpianos.com",
    facebook_link = "https://www.facebook.com/theduelingpianos",
    seeking_talent = False,
    image_link = "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
)

venue3 = Venue(
    name = "Park Square Live Music & Coffee",
    genres = ["Rock n Roll", "Jazz", "Classical", "Folk"],
    address = "34 Whiskey Moore Ave",
    city = "San Francisco",
    state = "CA",
    phone = "415-000-1234",
    website = "https://www.parksquarelivemusicandcoffee.com",
    facebook_link = "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent = False,
    image_link = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
)

artist1 = Artist(
    name = "Guns N Petals",
    genres = ["Rock n Roll"],
    city = "San Francisco",
    state = "CA",
    phone = "326-123-5000",
    website = "https://www.gunsnpetalsband.com",
    facebook_link = "https://www.facebook.com/GunsNPetals",
    seeking_venue = True,
    seeking_description = "Looking for shows to perform at in the San Francisco Bay Area!",
    image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
)

artist2 = Artist(
    name = "Matt Quevedo",
    genres = ["Jazz"],
    city = "New York",
    state = "NY",
    phone = "300-400-5000",
    facebook_link = "https://www.facebook.com/mattquevedo923251523",
    seeking_venue = False,
    image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
)

artist3 = Artist(
    name = "The Wild Sax Band",
    genres = ["Jazz", "Classical"],
    city = "San Francisco",
    state = "CA",
    phone = "432-325-5432",
    seeking_venue = False,
    image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
)


db.session.close()
db.drop_all()
db.create_all()

db.session.add(venue1)
db.session.add(venue2)
db.session.add(venue3)
db.session.add(artist1)
db.session.add(artist2)
db.session.add(artist3)

db.session.commit()

# now that we have committed the artist/venues, they now have non-null Ids, so we can add the shows

show1 = Show(
    start_time = "2019-05-21T21:30:00.000Z",
    artist_id = artist1.id,
    venue_id = venue1.id
)

show2 = Show(
    start_time = "2019-06-15T23:00:00.000Z",
    artist_id = artist2.id,
    venue_id = venue3.id
)

show3 = Show(
    start_time = "2035-04-01T20:00:00.000Z",
    artist_id = artist3.id,
    venue_id = venue3.id
)

show4 = Show(
    start_time = "2035-04-08T20:00:00.000Z",
    artist_id = artist3.id,
    venue_id = venue3.id
)

show5 = Show(
    start_time = "2035-04-15T20:00:00.000Z",
    artist_id = artist3.id,
    venue_id = venue3.id
)

db.session.add(show1)
db.session.add(show2)
db.session.add(show3)
db.session.add(show4)
db.session.add(show5)

db.session.commit()
