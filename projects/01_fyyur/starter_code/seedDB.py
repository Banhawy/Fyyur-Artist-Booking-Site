from helper_functions import seed_db
from app import db, Artist, Venue, Show, Genre, Venue_Genre, Artist_Genre

# SEED DB
seed_db(db, Artist, Venue, Show, Genre, Venue_Genre, Artist_Genre)
