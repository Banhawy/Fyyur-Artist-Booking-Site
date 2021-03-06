#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import logging
import sys
import uuid
from logging import FileHandler, Formatter

import babel
import dateutil.parser
from flask import (Flask, Response, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from sqlalchemy.dialects.postgresql import UUID

from forms import *
from helper_functions import (error_logger, format_artist_data,
                              format_artist_page_data, format_show_data,
                              format_venue_page_data, get_future_shows_count,
                              get_past_shows, get_past_shows_count, search_results_format,
                              get_upcoming_shows, get_venue_data, seed_db)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# DONE: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500), default='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60')
    facebook_link = db.Column(db.String(120))
    # DONE: implement any missing fields, as a database migration using Flask-Migrate
    website= db.Column(db.String(120), default='www.example.com')
    seeking_talent = db.Column(db.Boolean,  nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
    genres = db.relationship('Venue_Genre', backref='venue', lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
    def __repr__(self):
      return '<Venue ' + str(self.id) + ' ' + self.name + '>'

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500), default='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80')
    facebook_link = db.Column(db.String(120))
    # DONE: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(500), default='www.example.com')
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
    genres = db.relationship('Artist_Genre', backref='artist', lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
    def __repr__(self):
      return '<Artist ' + str(self.id) + ' ' + self.name + '>'
    
# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'show'
  
  artist_id = db.Column(db.String, db.ForeignKey('artist.id', ondelete='CASCADE'), primary_key=True)
  venue_id = db.Column(db.String, db.ForeignKey('venue.id', ondelete='CASCADE'), primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False, primary_key=True)

class Genre(db.Model):
  __tablename__ = 'genre'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  venue_genre = db.relationship('Venue_Genre', backref='genres', lazy=True)
  artist_genre = db.relationship('Artist_Genre', backref='genres', lazy=True)
  def __repr__(self):
      return '<Genre ' + str(self.id) + ' ' + self.name + '>'
  
class Venue_Genre(db.Model):
  __tablename__ = 'venue_genre'
  
  venue_id = db.Column(db.String, db.ForeignKey('venue.id', ondelete='CASCADE'), primary_key=True)
  genre = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
  
class Artist_Genre(db.Model):
  __tablename__ = 'artist_genre'
  
  artist_id = db.Column(db.String, db.ForeignKey('artist.id', ondelete='CASCADE'), primary_key=True)
  genre = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
  
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
      date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  try:
    venues = Venue.query.order_by(Venue.state).all()
    data = get_venue_data(venues)
  except Exception as e:
    error_logger(e, 'Error in venue listing')
  finally:
    db.session.close()
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  try:
    search_query = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
    result_data = search_results_format(db, Show, search_query, 'venue')
    db.session.close()
    return render_template('pages/search_venues.html', results=result_data, search_term=search_term)
  except Exception as e:
    error_logger(e, 'Error searching venue')
    flash('Error searching venue')
    return render_template('pages/search_venues.html', results={}, search_term=search_term)
    

@app.route('/venues/<string:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
   # Query all artists and return Artist list in JSON object to client requesting '/artists/all' endpoint
  if venue_id == 'all':
    error = False
    try:
      venues = Venue.query.all()
    except Exception as e:
      error_logger(e, 'Error fetching venues for select options')
      error = True
    finally:
      if error:
        return abort(400)
      else:
        body = {}
        venues_list = []
        body["venues_list"] = []
        for venue in venues:
          venue_obj = {
            "venue_id": venue.id,
            "venue_name": venue.name
          }
          venues_list.append(venue_obj)
        body["venues_list"] = venues_list
        return jsonify(body)

  error = False
  try:
    venue = Venue.query.get(venue_id)
  except Exception as e:
    error_logger(e, 'Error fetching venue ' + venue_id)
    error = True
  finally:
    db.session.close()
    if not error:
      future_shows = get_upcoming_shows(db, Show, Venue, Artist, venue_id, 'venue')
      future_shows_count = get_future_shows_count(db, Show, venue_id, 'venue')
      past_shows = get_past_shows(db, Show, Venue, Artist, venue_id, 'venue')
      past_shows_count = get_past_shows_count(db, Show, venue_id, 'venue')

      venue = Venue.query.get(venue_id)
      venue_data = format_venue_page_data(db, Genre, venue, future_shows, future_shows_count, 
                              past_shows, past_shows_count)
      return render_template('pages/show_venue.html', venue=venue_data)
    else:
      flash('Oops! An error occured while fetching the venue page')
      return render_template('pages/home.html')


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    fb_link = request.form['facebook_link']
    website = request.form['website']
    if 'seeking_talent' in request.form:
      seeking_talent = True 
    else:
      seeking_talent = False
    seeking_description = request.form['seeking_description']
    v_id = uuid.uuid1()
    new_venue = Venue(id=v_id, 
                      name=name, 
                      city=city, 
                      state=state, 
                      address=address, 
                      phone=phone, 
                      facebook_link=fb_link, 
                      website=website,
                      seeking_talent=seeking_talent, 
                      seeking_description=seeking_description)
    db.session.add(new_venue)
    for genre in genres:
      # get the id of the genre from the genre table in db
      genre_id = Genre.query.filter_by(name=genre).first().id
      # store the venue-genre combination in db
      new_genre = Venue_Genre(venue_id=v_id, genre=genre_id)
      db.session.add(new_genre)
    db.session.commit()
  except Exception as e:
    error_logger(e, 'Error in venue creation')
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    # on successful db insert, flash success
    if error:
      message = 'There was an error listing the Venue'
    else:
      message = 'Venue ' + request.form['name'] + ' was successfully listed!'
    flash(message)
    # DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')
    

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except Exception as e:
    error_logger(e, 'Error in venue deletion')
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      return jsonify({ 'success': False })
    else:
      return jsonify({ 'success': True })
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  error = False
  try:
    artists = Artist.query.add_columns('id', 'name').all()
    data = format_artist_data(artists)
  except Exception as e:
    error_logger(e, 'Error in artist listing')
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      return render_template('errors/500.html')
    else:
      return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  try:
    search_query = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
    result_data = search_results_format(db, Show, search_query, 'artist')
    db.session.close()
    return render_template('pages/search_artists.html', results=result_data, search_term=search_term)
  except Exception as e:
    error_logger(e, 'Error searching artist')
    flash('Error searching artist')
    return render_template('pages/search_artists.html', results={}, search_term=search_term)

@app.route('/artists/<string:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id

  # Query all artists and return Artist list in JSON object to client requesting '/artists/all' endpoint
  if artist_id == 'all':
    error = False
    try:
      artists = Artist.query.all()
    except Exception as e:
      error_logger(e, 'Error fetching artists for select options')
      error = True
    finally:
      if error:
        return abort(400)
      else:
        body = {}
        artists_list = []
        body["artists_list"] = []
        for artist in artists:
          artist_obj = {
            "artist_id": artist.id,
            "artist_name": artist.name
          }
          artists_list.append(artist_obj)
        body["artists_list"] = artists_list
        return jsonify(body)

  try:
    future_shows = get_upcoming_shows(db, Show, Venue, Artist, artist_id, 'artist')
    future_shows_count = get_future_shows_count(db, Show, artist_id, 'artist')
    past_shows = get_past_shows(db, Show, Venue, Artist, artist_id, 'artist')
    past_shows_count = get_past_shows_count(db, Show, artist_id, 'artist')

    artist = Artist.query.get(artist_id)
    data = format_artist_page_data(db, Genre, artist, future_shows, future_shows_count, past_shows, past_shows_count)
    return render_template('pages/show_artist.html', artist=data)
  except Exception as e:
    error_logger(e, 'Error fetching artist data')
    flash('Error fetching artist data')
    return render_template('pages/home.html')


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  error = False
  try:
    artist_data = Artist.query.get(artist_id)
    artist = format_artist_page_data(db, Genre, artist_data)
  except Exception as e:
    error_logger(e, 'Failed to editing artist ' + artist_id )
    error = True
  finally:
    db.session.close()
    if error:
      return redirect(url_for('show_artist', artist_id=artist_id))
    else:
      # DONE: populate form with fields from artist with ID <artist_id>
      return render_template('forms/edit_artist.html', form=form, artist=artist)
      

@app.route('/artists/<artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    artist = Artist.query.get(artist_id)
    name = request.form['name']
    state = request.form['state']
    city = request.form['city']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    seeking_description = request.form['seeking_description']
    
    artist.name = name
    artist.state = state
    artist.city = city
    artist.phone = phone
    artist.facebook_linke = facebook_link
    artist.website = website
    if 'seeking_venue' in request.form:
      artist.seeking_venue = True
    else:
      artist.seeking_venue = False
    artist.seeking_description = seeking_description

    db.session.commit()
  except Exception as e:
    error = True
    error_logger(e, 'Error updating artist ' + artist_id)
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      message = 'Error updating Artist'
    else:
      message = 'Successfully updated Artist'
    flash(message)
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # DONE: populate form with values from venue with ID <venue_id>
  error = False
  try:
    venue_data = Venue.query.get(venue_id)
    venue = format_venue_page_data(db, Genre, venue_data)
  except Exception as e:
    error_logger(e, 'Failed to editing venue ' + venue_id )
    error = True
  finally:
    db.session.close()
    if error:
      flash('Could not fetch venue to edit')
      return redirect(url_for('show_venue', venue_id=venue_id))
    else:
      return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    venue = Venue.query.get(venue_id)
    name = request.form['name']
    state = request.form['state']
    city = request.form['city']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    seeking_description = request.form['seeking_description']
    
    venue.name = name
    venue.state = state
    venue.city = city
    venue.phone = phone
    venue.facebook_link = facebook_link
    venue.website = website
    if 'seeking_talent' in request.form:
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False
    venue.seeking_description = seeking_description

    db.session.commit()
  except Exception as e:
    error = True
    error_logger(e, 'Error updating venue ' + venue_id)
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      message = 'Error updating Venue'
    else:
      message = 'Successfully updated Venue'
    flash(message)
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: modify data to be the data object returned from db insertion
  error = False
  try:
    name = request.form['name']
    state = request.form['state']
    city = request.form['city']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    fb_link = request.form['facebook_link']
    website = request.form['website']
    if 'seeking_venue' in request.form:
      seeking_venue = True 
    else:
      seeking_venue = False
    seeking_description = request.form['seeking_description']
    a_id = uuid.uuid1()
    new_artist = Artist(id=a_id, 
                        name=name, 
                        city=city, 
                        state=state, 
                        phone=phone, 
                        facebook_link=fb_link, 
                        website=website, 
                        seeking_venue=seeking_venue, 
                        seeking_description=seeking_description)
    db.session.add(new_artist)
    for genre in genres:
      # get the id of the genre from the genre table in db
      genre_id = Genre.query.filter_by(name=genre).first().id
      # store the venue-genre combination in db
      new_artist_genre = Artist_Genre(artist_id=a_id, genre=genre_id)
      db.session.add(new_artist_genre)
    db.session.commit()
  except Exception as e:
    error_logger(e, 'Error in artist creation')
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    # on successful db insert, flash success
    if error:
      message = 'There was an error listing Artist'
    else:
      message = 'Artist ' + name + ' was successfully listed!'
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  flash(message)
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  join_query = db.session.query(Show, Artist, Venue).\
                          filter(Show.artist_id == Artist.id).\
                          filter(Show.venue_id == Venue.id).\
                          all()
  show_data = format_show_data(join_query)
  return render_template('pages/shows.html', shows=show_data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  error = False
  try:
    venue_id = request.form['venue_id']
    artist_id = request.form['artist_id']
    start_time = request.form['start_time']
    new_show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(new_show)
    db.session.commit()
  except Exception as e:
    error_logger(e, 'Error in show creation')
    db.session.rollback()
    error = True
  finally:
    db.session.close()
    if error:
      message = 'An error occured while creating show'
    else:
      message = 'Successfully created a new show'
    # on successful db insert, flash success
    flash(message)
    # DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

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
  app.run(host='0.0.0.0', debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
