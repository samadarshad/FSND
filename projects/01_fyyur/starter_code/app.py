#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from forms import *
from models import *
from util import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
db.app = app
from venue import venue_api
from artist import artist_api
from show import show_api
from artist_availability import artist_availability_api
app.register_blueprint(venue_api, url_prefix='/venues')
app.register_blueprint(artist_api, url_prefix='/artists')
app.register_blueprint(show_api, url_prefix='/shows')
app.register_blueprint(artist_availability_api, url_prefix='/artists')
migrate = Migrate(app, db, compare_type=True)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

def getMostRecentlyListedItems():
    a = db.session.query(Artist.name, Artist.id, Artist.creation_date, sqlalchemy.sql.expression.literal(Artist.__tablename__).label("tablename"))
    v = db.session.query(Venue.name, Venue.id, Venue.creation_date, sqlalchemy.sql.expression.literal(Venue.__tablename__).label("tablename"))
  
    assert(a.union(v).order_by(Artist.creation_date.desc()).all() == a.union(v).order_by(Venue.creation_date.desc()).all())

    most_recent_items = a.union(v).order_by(Artist.creation_date.desc()).limit(10).all()
    return most_recent_items

@app.route('/')
def index():
    recentItems = getMostRecentlyListedItems()
    return render_template('pages/home.html', recentItems=recentItems)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
