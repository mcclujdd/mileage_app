#mileage_2.0.py
#take user input to help track mileage for import
# to google sheets mileage worksheet


from datetime import date
import location
import time
import options
import functions as func

#load configurations
import _config as config
import logging
logging.basicConfig(filename=config.log_file, level=logging.DEBUG)
output_file = config.output_file
loc2loc_miles = config.loc2loc_miles
loc_zips = config.loc_zips
home_loc = config.HOME_LOC
print( '\n#\nHere we go...')
print(f'Configurations loaded. Outputting to {output_file}\n')

today = date.today()
date = today.strftime("%m/%d/%y")
entry_headers = ['date', 'startloc', 'endloc', 'startodo', 'endodo', 'tripmiles']
default_entry = [date, 'HM', home_loc, 0, 0, 0]




def exec_opt(opt, *args):
  if opt in options.opts:
    # dict to select option like switch stamement?
      if opt == 'a':
          func.exec_a_loop()
      else:
          options.opts[opt].execute()
  else:
    print(f'Command {opt} not valid. h for help. ')


def main():
  
  
  while True:
    print('\n~>Please select an option (h - help):')
    p = func.parse_input(input('$'))
    exec_opt(p[0])
  exit()
  


if __name__ == "__main__":
  main()










  #deprecated
  while True:

    last_entry = get_last_entry(output_file)
    start_loc = last_known_loc
    end_loc = ''

    if last_entry.get('date') != date and entries[-1].get('date') != date:

      if last_entry['endloc'] != 'LL':
        final = [last_entry['date'], last_entry['endloc'], 'LL', last_entry['endodo'], last_entry['endodo']+ get_loc2loc_miles(last_entry['endloc'], 'LL'), get_loc2loc_miles(last_entry['endloc'], home_loc)]
        final = create_entry(final)
        append_file(output_file, final)
        print(f'Missing final trip added to previous date.\n{final}\n')

      entries = [] #remove earlier than today entries
      entries.append(create_entry([date, 'HM', home_loc, 1, 1, get_loc2loc_miles('HM', home_loc)]))

    prior_entry = [entries[-1].get(item) for item in entries[-1]]
    print(f'LAST ENTRY: {prior_entry}')
    end_odo = set_odo()

    if end_odo == 1: #get missing trip info and add to list of entries
      end_loc = input('Location > ').strip().upper()
      start_loc = entries[-1].get('endloc')
      entries.append(create_entry([date, start_loc, end_loc, 1, end_odo, get_loc2loc_miles(start_loc, end_loc)]))
      continue
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
