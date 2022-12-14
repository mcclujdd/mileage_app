import _config
import location, time
from Exceptions import *
import c_trips


def exec_a_loop():
  while True:
    u_input=parse_input(input("Enter Trip Data:"))
    try:
      create_entry(u_input)
      entry = clean_manual_input(*u_input)
      break
    except (IndexError, ValidationError) as err:
      print(err)
  append_file(entry)


def create_entry(entry: list, file=_config.output_file)->dict:
  #ensure uppercase locations
  try:
    assert len(entry) == 6
  except AssertionError:
    print('Invalid: Must input 6 values. h a for help.')
    return 
  entry[1] = entry[1].upper()
  entry[2] = entry[2].upper()
  try:
    entry[3] = int(entry[3])
    entry[4] = int(entry[4])
    entry[5] = int(entry[5])
  except Exception as e:
    print('Invalid: Must use integers as final 3 values.')
    return 
  trip = c_trips.Trip()
  #new and testing
  errors = trip.validate_data(entry)
  try:
    assert len(errors) < 1
  except Exception as e:
    print('Validation Errors:\n')
    for err in errors: print(f'>>{err}')
    return
  
  

########################################
'''needs testing'''


def parse_input(input):
  _ = input.split()
  return _
  
  
def clean_manual_input(*args) -> dict:
  output = []
  headers = _config.ENTRY_HEADERS

  for a in range(3):
    try:
      output.append(str(args[a]))
    except ValueError as ve:
      print(ve)
      raise ValueError()

    except IndexError as ie:
      print('Input requires 6 arguments. Please try again.')
      raise IndexError

  for a in range(3):
    try:
      #check odometers to read   a<b and c=b-c
      output.append(int(args[a + 3]))
    except ValueError as ve:
      raise ValueError(f'{ve}: Please check values for accurate formatting.')

    except IndexError as ie:
      print('Input requires 6 arguments. Please try again.')

  output = dict(zip(headers, output))

  return output
  
def get_current_zipcode()->str:
  print('Identifying location....')
  location.start_updates()
  time.sleep(3)
  loc = location.get_location()
  addr = location.reverse_geocode(loc)
  location.stop_updates()
  return addr[0].get('ZIP') #zipcode as str
  
def get_loc_from_zip(zipcode):
  if zipcode in _config.loc_zips:
    loc = _config.loc_zips.get(zipcode,)
    if isinstance(loc, list):
      for _ in loc:
        print('\t- '+ _)
      end_loc = input('Multiple locations found: input a speceific location from above >').upper().strip()
    else:
      end_loc = loc
  else:
    end_loc = input('Current Location > ').strip().upper()
  return end_loc
  
def get_loc2loc_miles(loc1, loc2):
  key = loc1+loc2
  try:
    if not type(loc2loc_miles.get(key)) == int:
      raise ValueError
  except ValueError:
    print(f'ERROR: {key} trip returned {loc2loc_miles.get(key)} as a value for miles.')
    exit()
  return loc2loc_miles.get(key)


########################################
'''maybe useful'''

def get_last_entry(filename, headers = _config.ENTRY_HEADERS):
#       last_years_file = gen_last_year_file(filename)
  with open(filename, 'r') as file:
    last_entry = file.readlines()[-1].strip().split(', ')

#               if last_entry == ENTRY_HEADERS:
#                       return get_last_entry(last_years_file)
#               else:
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



