from app import db, Artist, Venue
from helper_functions import error_logger

def get_artists_choices():
  artists_data = []
  try:
    artists = Artist.query.add_columns('id', 'name').all()
    for artist_tuple in artists:
        # artist tuple comes in the form (<Artist query object> , 'uuid-string', 'Artist Name')
        split_id_string = artist_tuple[1].split('-')
        shortened_id = split_id_string[0] + '...' + split_id_string[-1]
        artist_name = artist_tuple[2]
        combined_display_string = shortened_id + ': ' + artist_name
        modified_tuple = (artist_tuple[1], combined_display_string)
        artists_data.append(modified_tuple)
  except Exception as e:
    error_logger(e, 'Error getting artists choices')
  finally:
    db.session.close()
    return artists_data

def get_venue_choices():
  venue_data = []
  try:
    venue = Venue.query.add_columns('id', 'name').all()
    for venue_tuple in venue:
        # venue tuple comes in the form (<Venue query object> , 'uuid-string', 'Venue Name')
        split_id_string = venue_tuple[1].split('-')
        shortened_id = split_id_string[0] + '...' + split_id_string[-1]
        venue_name = venue_tuple[2]
        combined_display_string = shortened_id + ': ' + venue_name
        modified_tuple = (venue_tuple[1], combined_display_string)
        venue_data.append(modified_tuple)
  except Exception as e:
    error_logger(e, 'Error getting venue choices')
  finally:
    db.session.close()
    return venue_data