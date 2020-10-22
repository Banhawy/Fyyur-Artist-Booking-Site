import traceback
import logging
from sqlalchemy import func
from datetime import datetime

def error_logger(e, message):
  logging.error(traceback.format_exc)
  print(e.__doc__)
  print(e.message)
  print(message)

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

def format_venue_page_data(venue, genre_dict):
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
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0
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

def format_artist_page_data(artist, future_shows, future_shows_count, past_shows, past_shows_count, genre_dict):
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
  data["seeking_venue"] = artist.seeking_venue
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

def get_future_shows_count(db, Show, artist_id):
  current_date = datetime.today().isoformat()
  # query retuns a tuple in the form (artist_id, future_show_count) 
  # e.x. (u'fd407ea1-1253-11eb-b418-18a905365095', 3L)
  filtered_query = db.session.query(Show.artist_id, func.count(Show.start_time))\
                              .select_from(Show).filter(Show.start_time > current_date)\
                              .filter(Show.artist_id == artist_id)\
                              .group_by(Show.artist_id)\
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

# Given an artist_id return a list of upcoming shows venue data
def get_upcoming_shows(db, Show, Venue, artist_id):
  data = []
  current_date = datetime.today().isoformat()
  # get venue name & image_link
  upcoming_shows = Show.query.filter(Show.start_time > current_date)\
                              .filter(Show.artist_id == artist_id)\
                              .all()
  for show in upcoming_shows:
    start_time = show.start_time
    venue_id = show.venue_id
    venue_name, venue_image_link = get_venue_name_image(db, Venue, venue_id)
    
    venue_obj = {}
    venue_obj["venue_id"] = venue_id
    venue_obj["venue_name"] = venue_name
    venue_obj["venue_image_link"] = venue_image_link
    venue_obj["start_time"] = start_time
    
    data.append(venue_obj)
  
  return data

# Given an artist_id return a list of past shows venue data
def get_past_shows(db, Show, Venue, artist_id):
  data = []
  current_date = datetime.today().isoformat()
  # get venue name & image_link
  past_shows = Show.query.filter(Show.start_time < current_date)\
                              .filter(Show.artist_id == artist_id)\
                              .all()
  for show in past_shows:
    start_time = show.start_time
    venue_id = show.venue_id
    venue_name, venue_image_link = get_venue_name_image(db, Venue, venue_id)
    
    venue_obj = {}
    venue_obj["venue_id"] = venue_id
    venue_obj["venue_name"] = venue_name
    venue_obj["venue_image_link"] = venue_image_link
    venue_obj["start_time"] = start_time
    
    data.append(venue_obj)
  
  return data

def get_past_shows_count(db, Show, Venue, artist_id):
  current_date = datetime.today().isoformat()
  # query retuns a tuple in the form (artist_id, past_show_count) 
  # e.x. (u'fd407ea1-1253-11eb-b418-18a905365095', 3L)
  filtered_query = db.session.query(Show.artist_id, func.count(Show.start_time))\
                              .select_from(Show)\
                              .filter(Show.start_time < current_date)\
                              .filter(Show.artist_id == artist_id)\
                              .group_by(Show.artist_id)\
                              .first()
  if filtered_query is None: 
    count = 0 
  else:
    count = int(filtered_query[1])
  return count 