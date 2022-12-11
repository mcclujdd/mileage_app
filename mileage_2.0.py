#mileage_2.0.py
#take user input to help track mileage for import
#to google sheets mileage worksheet

from datetime import date
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


def main():
  
  user_options = options.opts
  while True:
    print('\n~>Please select an option (h - help):')
    p = func.parse_input(input('$'))
    if p[0] in user_options:
      if len(p) > 1:
        user_options[p[0]].execute(p[1])
      else:
        if p[0] == 'a':
          while p[0] == 'a':
            try:
              user_options[p[0]].execute(func.parse_input(input("Enter trip data:")))
              break
            except (IndexError, ValidationError) as err:
              print(err)
        else:
          user_options[p[0]].execute()

    else:
      print(f'Command {p[0]} not valid. h for help. ')
  exit()
  
class NoTripFound(BaseException):
  '''failure to find a value for trip in the dictionary per the config file'''
  pass

class ValidationError(BaseException):
  '''Failure to validate data format'''

if __name__ == "__main__":
  main()
