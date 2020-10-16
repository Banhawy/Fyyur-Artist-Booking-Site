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