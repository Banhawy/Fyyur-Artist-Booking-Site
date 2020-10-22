import traceback
import logging
import uuid
from sqlalchemy import func
from datetime import datetime

def error_logger(e, message):
  logging.error(traceback.format_exc)
  print(e.__doc__)
  if hasattr(e, 'message'):
    print(e.message)
  print(message)

# Return a list of Venue_Genres
def generate_venue_genres(Venue_Genre, genre_dict, venue_id, genre_list):
  venue_genres = []
  genre_id_dict = {}
  for genre_id, genre_name in genre_dict.items():
    genre_id_dict[genre_name] = genre_id
  for genre_name in genre_list:
    genre_id = genre_id_dict[genre_name]
    venue_genre = Venue_Genre(venue_id=venue_id, genre=genre_id)
    venue_genres.append(venue_genre)
  return venue_genres

# Return a list of Artist_Genres
def generate_artist_genres(Artist_Genre, genre_dict, artist_id, genre_list):
  artist_genres = []
  genre_id_dict = {}
  for genre_id, genre_name in genre_dict.items():
    genre_id_dict[genre_name] = genre_id
  for genre_name in genre_list:
    genre_id = genre_id_dict[genre_name]
    artist_genre = Artist_Genre(artist_id=artist_id, genre=genre_id)
    artist_genres.append(artist_genre)
  return artist_genres

def seed_db(db, Artist, Venue, Show, Genre, Venue_Genre, Artist_Genre, genre_dict):
  #  Genres
  #  ----------------------------------------------------------------
  # Seed Genres table
  genres = ['Jazz', 'Classical', 'Reggae', 'Alternative', 'Country', 'Electronic', 'Folk', 'Funk', 'Soul', 'Hip-Hop', 'Heavy Metal', 'Instrumental', 'Musical Theatre', 'Pop', 'Punk', 'Blues', 'R&B', 'Rock n Roll', 'Other']
  for genre in genres:
    query_count = Genre.query.filter_by(name=genre).count()
    if query_count == False:
      try:
        new_genre = Genre(name=genre)
        db.session.add(new_genre)
        db.session.commit()
      except Exception as e:
        error_logger(e, 'Error in genre seeding')
        db.session.rollback()
      finally:
        db.session.close()
    
  #  Venues
  #  ----------------------------------------------------------------  
  # Seed Venues table if empty
  v_id1 = str(uuid.uuid4())
  v_id2 = str(uuid.uuid4())
  v_id3 = str(uuid.uuid4())
  if Venue.query.count() == 0:
    venue1 = Venue(id=v_id1, name="The Musical Hop", address="1015 Folsom Street", city="San Fransisco",
                  state="CA", phone="123-123-1234", website="https://www.themusicalhop.com",
                  facebook_link="https://www.facebook.com/TheMusicalHop", seeking_talent=True,
                  seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
                  image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")
    venue2 = Venue(id=v_id2, name="The Dueling Pianos Bar", address="335 Delancey Street", city="New York",
                  state="NY", phone="914-003-1132", website="https://www.theduelingpianos.com",
                  facebook_link="https://www.facebook.com/theduelingpianos", seeking_talent=False,
                  image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80")
    venue3 = Venue(id=v_id3, name="Park Square Live Music & Coffee", address="34 Whiskey Moore Ave", city="San Fransisco",
                  state="CA", phone="415-000-1234", website="https://www.parksquarelivemusicandcoffee.com",
                  facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee", seeking_talent=False,
                  image_link="")
    try:
      db.session.add_all([venue1, venue2, venue3])
      db.session.commit()
    except Exception as e:
      error_logger(e, 'Error in Venue seeding')
      db.session.rollback()

    # Seed Venue_Genre table
    venue1_genres = ["Jazz", "Reggae", "Other", "Classical", "Folk"]
    venue2_genres = ["Classical", "R&B", "Hip-Hop"]
    venue3_genres = ["Rock n Roll", "Jazz", "Classical", "Folk"]
    venue_genre_list1 = generate_venue_genres(Venue_Genre, genre_dict, v_id1, venue1_genres)
    venue_genre_list2 = generate_venue_genres(Venue_Genre, genre_dict, v_id2, venue2_genres)
    venue_genre_list3 = generate_venue_genres(Venue_Genre, genre_dict, v_id3, venue3_genres)
    venue_genres_all = venue_genre_list1 + venue_genre_list2 + venue_genre_list3
    try:
      db.session.add_all(venue_genres_all)
      db.session.commit()
    except Exception as e:
      error_logger(e, 'Error in Venue Genre seeding')
      db.session.rollback()
  
  #  Artists
  #  ----------------------------------------------------------------
  # Seed Artist table if empty
  a_id1 = str(uuid.uuid4())
  a_id2 = str(uuid.uuid4())
  a_id3 = str(uuid.uuid4())
  if Artist.query.count() == 0:
    artist1 = Artist(id=a_id1, name="Guns N Petals", city="San Fransisco", state="CA", 
                  phone="326-123-5000", website="https://www.gunsnpetalsband.com",
                  facebook_link="https://www.facebook.com/GunsNPetals", seeking_venue=True,
                  seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
                  image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")
    artist2 = Artist(id=a_id2, name="Matt Quevedo", city="New York", state="NY", phone="300-400-5000",
                  facebook_link="https://www.facebook.com/mattquevedo923251523", seeking_venue=False,
                  image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80")
    artist3 = Artist(id=a_id3, name="The Wild Sax Band", city="San Fransisco", state="CA", 
                  phone="432-325-5432", seeking_venue=False,
                  image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80")
    try:
      db.session.add_all([artist1, artist2, artist3])
      db.session.commit()
    except Exception as e:
      error_logger(e, 'Error in Artist seeding')
      db.session.rollback()

    # Seed Artist_Genre table
    artist1_genres = ["Rock n Roll"]
    artist2_genres = ["Jazz"]
    artist3_genres = ["Jazz", "Classical"]
    artist_genre_list1 = generate_artist_genres(Artist_Genre, genre_dict, a_id1, artist1_genres)
    artist_genre_list2 = generate_artist_genres(Artist_Genre, genre_dict, a_id2, artist2_genres)
    artist_genre_list3 = generate_artist_genres(Artist_Genre, genre_dict, a_id3, artist3_genres)
    artist_genres_all = artist_genre_list1 + artist_genre_list2 + artist_genre_list3
    try:
      db.session.add_all(artist_genres_all)
      db.session.commit()
    except Exception as e:
      error_logger(e, 'Error in Artist Genre seeding')
      db.session.rollback()

  #  Shows
  #  ----------------------------------------------------------------
  if Show.query.count() == 0:
    show1 = Show(venue_id=v_id1, artist_id=a_id1, start_time="2019-05-21T21:30:00.000Z")
    show2 = Show(venue_id=v_id3, artist_id=a_id2, start_time="2019-06-15T23:00:00.000Z")
    show3 = Show(venue_id=v_id3, artist_id=a_id3, start_time="2035-04-01T20:00:00.000Z")
    show4 = Show(venue_id=v_id3, artist_id=a_id3, start_time="2035-04-15T20:00:00.000Z")
    try:
      db.session.add_all([show1, show2, show3, show4])
      db.session.commit()
    except Exception as e:
      error_logger(e, 'Error in Show seeding')
      db.session.rollback()
    finally:
      db.session.close()

# The function recievies a list of venues data fetched from DB
# and returns a list of sorted data organized by city, state
def get_venue_data(venues_list):
  data = []
  tuple_set = set()
  for x in venues_list:
    if (x.city, x.state) not in tuple_set:
      tuple_set.add((x.city, x.state))
      data.append({'city': x.city, 'state': x.state, 'venues': [{'id': x.id, 'name':x.name, 'num_upcoming_shows': 0}]})
    else:
      for y in data:
        if y['city'] == x.city and y['state'] == x.state:
          y['venues'].append({'id': x.id, 'name': x.name, 'upcoming_shows': 0})
  return data

def format_venue_page_data(venue, genre_dict, future_shows=[], future_shows_count=0, past_shows=[], past_shows_count=0):
  genre_list = []
  for venue_genre in venue.genres:
    genre_name = genre_dict[venue_genre.genre]
    genre_list.append(genre_name)
  venue_data = {
    "id": venue.id,
    "name": venue.name,
    "genres": genre_list,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "address": venue.address,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": future_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": future_shows_count
  }
  return venue_data

def format_artist_data(artists):
  data = []
  for artist_tuple in artists:
    artist_object = {
      "id": artist_tuple[1],
      "name": artist_tuple[2]
    }
    data.append(artist_object)
  return data

def format_artist_page_data(artist, genre_dict, future_shows=[], future_shows_count=0, past_shows=[], past_shows_count=0):
  data = {}
  genre_list = []
  for genre in artist.genres:
    genre_name = genre_dict[genre.genre]
    genre_list.append(genre_name)
  data["id"] = artist.id
  data["name"] = artist.name
  data["genres"] = genre_list
  data["city"] = artist.city
  data["state"] = artist.state
  data["phone"] = artist.phone
  data["facebook_link"] = artist.facebook_link
  data["seeking_venue"] = artist.seeking_venue
  data["seeking_description"] = artist.seeking_description
  data["image_link"] = artist.image_link
  data["past_shows"] = past_shows
  data["upcoming_shows"] = future_shows
  data["past_shows_count"] = past_shows_count
  data["upcoming_shows_count"] = future_shows_count
  return data

# Formats joined query data and returns a list of show data
def format_show_data(joined_show_artist_venue_data):
  data = []
  for show , artist, venue in joined_show_artist_venue_data:
    show_data = {}
    show_data["venue_id"] = show.venue_id
    show_data["venue_name"] = venue.name
    show_data["artist_id"] = artist.id
    show_data["artist_name"] = artist.name
    show_data["artist_image_link"] = artist.image_link
    show_data["start_time"] = show.start_time.isoformat()
    data.append(show_data)
  return data

def get_future_shows_count(db, Show, id, id_type):
  if id_type == 'artist':
    show_id = Show.artist_id
  elif id_type == 'venue':
    show_id = Show.venue_id
  else:
    show_id = Show.artist_id
  current_date = datetime.today().isoformat()
  # query retuns a tuple in the form (artist_id/venue_id, future_show_count) 
  # e.x. (u'fd407ea1-1253-11eb-b418-18a905365095', 3L)
  filtered_query = db.session.query(show_id, func.count(Show.start_time))\
                              .select_from(Show).filter(Show.start_time > current_date)\
                              .filter(show_id == id)\
                              .group_by(show_id)\
                              .first()
  if filtered_query is None: 
    count = 0 
  else:
    count = int(filtered_query[1])
  return count 

# Given a venue_id returns a tuple with venue name and venue image link
def get_venue_name_image(db, Venue, venue_id):
  venue = Venue.query.get(venue_id)
  return (venue.name, venue.image_link)

# Given an artist_id returns a tuple with artist name and artist image link
def get_artist_name_image(db, Artist, artist_id):
  artist = Artist.query.get(artist_id)
  return (artist.name, artist.image_link)

# Given an artist_id/venue_id return a list of upcoming shows venue data
def get_upcoming_shows(db, Show, Venue, Artist, id, id_type):
  data = []
  current_date = datetime.today().isoformat()
  if id_type == 'artist':
    show_id = Show.artist_id
  elif id_type == 'venue':
    show_id = Show.venue_id
  else:
    show_id = Show.artist_id
  # get venue name & image_link
  upcoming_shows = Show.query.filter(Show.start_time > current_date)\
                              .filter(show_id == id)\
                              .all()
  for show in upcoming_shows:
    start_time = show.start_time
    if id_type == 'artist':
      venue_id = show.venue_id
      venue_name, venue_image_link = get_venue_name_image(db, Venue, venue_id)
      
      venue_obj = {}
      venue_obj["venue_id"] = venue_id
      venue_obj["venue_name"] = venue_name
      venue_obj["venue_image_link"] = venue_image_link
      venue_obj["start_time"] = start_time
      data.append(venue_obj)

    elif id_type == 'venue':
      artist_id = show.artist_id
      artist_name, artist_image_link = get_artist_name_image(db, Artist, artist_id)
      
      artist_obj = {}
      artist_obj["artist_id"] = artist_id
      artist_obj["artist_name"] = artist_name
      artist_obj["artist_image_link"] = artist_image_link
      artist_obj["start_time"] = start_time
      data.append(artist_obj)

  return data

# Given an artist_id return a list of past shows venue data
def get_past_shows(db, Show, Venue, Artist, id, id_type):
  data = []
  current_date = datetime.today().isoformat()
  if id_type == 'artist':
    show_id = Show.artist_id
  elif id_type == 'venue':
    show_id = Show.venue_id
  else:
    show_id = Show.artist_id
  # get venue name & image_link
  past_shows = Show.query.filter(Show.start_time < current_date)\
                              .filter(show_id == id)\
                              .all()
  for show in past_shows:
    start_time = show.start_time
    if id_type == 'artist':
      venue_id = show.venue_id
      venue_name, venue_image_link = get_venue_name_image(db, Venue, venue_id)
      
      venue_obj = {}
      venue_obj["venue_id"] = venue_id
      venue_obj["venue_name"] = venue_name
      venue_obj["venue_image_link"] = venue_image_link
      venue_obj["start_time"] = start_time
      
      data.append(venue_obj)
    elif id_type == 'venue':
      artist_id = show.artist_id
      artist_name, artist_image_link = get_artist_name_image(db, Artist, artist_id)
      
      artist_obj = {}
      artist_obj["artist_id"] = artist_id
      artist_obj["artist_name"] = artist_name
      artist_obj["artist_image_link"] = artist_image_link
      artist_obj["start_time"] = start_time
      
      data.append(artist_obj)
    
  return data

def get_past_shows_count(db, Show, Venue, id, id_type):
  current_date = datetime.today().isoformat()
  if id_type == 'artist':
    show_id = Show.artist_id
  elif id_type == 'venue':
    show_id = Show.venue_id
  else:
    show_id = Show.artist_id

  # query retuns a tuple in the form (artist_id, past_show_count) 
  # e.x. (u'fd407ea1-1253-11eb-b418-18a905365095', 3L)
  filtered_query = db.session.query(show_id, func.count(Show.start_time))\
                              .select_from(Show)\
                              .filter(Show.start_time < current_date)\
                              .filter(show_id == id)\
                              .group_by(show_id)\
                              .first()
  if filtered_query is None: 
    count = 0 
  else:
    count = int(filtered_query[1])
  return count 