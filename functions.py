import _config
import time


def parse_input(input):
  _ = input.split()
  return _


def get_last_entry(filename, headers = _config.ENTRY_HEADERS):
#       last_years_file = gen_last_year_file(filename)
  with open(filename, 'r') as file:
    last_entry = file.readlines()[-1].strip().split(', ')
    for _ in last_entry:
      if last_entry.index(_) > 2:
        try:
          last_entry[last_entry.index(_)] = int(_)
        except:
          print(f'Error with format of {output_file}. Make sure the last three values are whole numbers (integers).')
          print('Exiting...')
          exit()
    try:
      if len(last_entry) != 6:
        raise NoTripFound
    except NoTripFound:
      print(f"ERROR: NoTripFound for last entry, check {output_file} formatting for 6 items. e.g.:\n1/1/70, AA, BB, 2000, 2100, 100")
      exit()

    entry = dict(zip(headers, last_entry))
    return entry


def set_last_known_loc():
  last_entry = get_last_entry(output_file)
  if last_entry.get('date') == date:
    return last_entry.get('endloc').strip()
  else:
    return 'HM'


def set_last_known_odo():
  f = get_last_entry(output_file)
  try:
    odo = int(f.get('endodo'))
  except ValueError:
    odo = 1
  return odo


def set_odo():
  while True:
    try:
      odo = int(input('Odometer > '))
      break
    except ValueError:
      print('Invalid entry. Please enter a number.')
      continue
  return odo


def append_file(entry, file=_config.output_file):
  print(f'Writing to {file}...')
  with open(file, 'a') as f:
    f.write(f"{entry['date']}, {entry['startloc']}, {entry['endloc']}, {entry['startodo']}, {entry['endodo']}, {entry['tripmiles']}\n")


def create_entry(entry):
  '''takes arg as list with 6 values in accordance with entry_headers and returns a dict with keys as entry headers and values as the 6 from arg'''
  trip = entry[1] + entry[2]
  try:
    if config.loc2loc_miles.get(trip) == None:
      raise NoTripFound
  except NoTripFound:
    print(f'Trip "{trip}" not found in _config.py. Exiting...')
    exit()
  new_entry = dict(zip(entry_headers, entry))
  return new_entry
  
  
