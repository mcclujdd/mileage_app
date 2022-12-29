import _config
import location, time, datetime
from Exceptions import *
import c_trips, options



def exec_a_loop():
  while True:
    u_input=parse_input(input("Enter Trip Data:"))
    if u_input[0] == "e":
      options.opts['e'].execute()
    try:
      validate_entry(u_input)
      entry = clean_manual_input(*u_input)
      break
    except (IndexError, ValidationError) as err:
      print(err)
  append_file(entry)


def validate_entry(entry: list, file=_config.output_file):
  # data validation function
  
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
  # give good errors for user
  errors = trip.validate_data(entry)
  try:
    assert len(errors) < 1
  except Exception as e:
    print('Validation Errors:\n')
    for err in errors: print(f'>>{err}')
    return
  
  

########################################
'''needs testing'''
def exec_opt(opt, *args):
  
  if opt in options.opts:
    # dict to select option like switch stamement?
      if opt == 'a':
          exec_a_loop()
      else:
          options.opts[opt].execute()
  else:
    print(f'Command {opt} not valid. h for help. ')

def parse_input(i):
  _ = i.split()
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
  loc2loc_miles = _config.loc2loc_miles
  try:
    if not type(loc2loc_miles.get(key)) == int:
      raise ValueError
  except ValueError:
    print(f'ERROR: {key} trip returned {loc2loc_miles.get(key)} as a value for miles.')
    exit()
  return loc2loc_miles.get(key)


def loc1_generator(last_entry):
  if last_entry.get('date') == _config.TODAY:
    return last_entry.get('loc2')
  else:
    return _config.HOME_LOC
    
def loc2_generator():
    return get_loc_from_zip(get_current_zipcode())

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

########################################

def deprecated_but_maybe_useful_for_m_option():
    #create object to store consecutive entries
    
    #add entries to object until user says they're done
    
    # display all edded entries with numbered indicators (for acting on a specific entry later)
    
    #functionality to remove entries
    
    #functionality to modify an entry
      #take user input (way to easily autogen the entry into the text field?)
    
    #populate odometer readings based off of any reading given
    
    #resort(manually?) so that entries can be added in any order
    
    if end_odo == 1: #get missing trip info and add to list of entries
      end_loc = input('Location > ').strip().upper()
      start_loc = entries[-1].get('endloc')
      entries.append(create_entry([date, start_loc, end_loc, 1, end_odo, get_loc2loc_miles(start_loc, end_loc)]))
      
    else: #get current trip info and back-calculate mileage readings
      missed_reading = False
      start_loc = entries[-1]['endloc']
      end_loc = get_loc_from_zip(get_current_zipcode())

      entries.append(create_entry([date, start_loc, end_loc, 1, end_odo, get_loc2loc_miles(start_loc, end_loc)]))

      '''try checking for a reading from current date with a valid odo and calculate all entry data based off of it'''
      entries.reverse()
      previous_end_odo = end_odo
      for entry in entries:
        if entry.get('date') == date:
          entry['endodo'] = int(previous_end_odo)
          entry['startodo'] = entry['endodo'] - entry['tripmiles']
          previous_end_odo = entry['startodo']

    entries.reverse()
    appended_entries = []
    for item in entries:
      if item['startloc'] != 'HM':
        append_file(output_file, item)
        appended_entries.append(item)
    print('\nENTRIES ADDED:')
    for item in appended_entries:
      print(item.get('date'), item.get('startloc'), item.get('endloc'), item.get('startodo'), item.get('endodo'), item.get('tripmiles'))
