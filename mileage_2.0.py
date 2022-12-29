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


TODAY = config.TODAY
entry_headers = ['date', 'startloc', 'endloc', 'startodo', 'endodo', 'tripmiles']
default_entry = [date, 'HM', home_loc, 0, 0, 0]




def main():
   
  while True:
    print('\n~>Please select an option (h - help):')
    p = func.parse_input(input('$'))
    try:
      func.exec_opt(p[0])
    except Exception as e:
      print(f'ERROR: {e}')
  

if __name__ == "__main__":
  main()
