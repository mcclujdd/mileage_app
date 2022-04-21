'''
take user input to help track mileage for import
 to google sheets mileage worksheet
'''

from datetime import date
import location
import time

#load configurations
import _config as config
output_file = config.output_file
loc2loc_miles = config.loc2loc_miles
loc_zips = config.loc_zips
home_loc = config.HOME_LOC
print( '\n#'*2)
print(f'Configurations loaded. Outputting to {output_file}\n')

today = date.today()
date = today.strftime("%m/%d/%y")

entry_headers = ['date', 'startloc', 'endloc', 'startodo', 'endodo', 'tripmiles']
default_entry = [date, 'HM', home_loc, 0, 0, 0]

class NoTripFound(Exception):
	'''failure to find a value for trip in the dictionary per the config file'''
	pass
	

def gen_last_year_file(file):
	no_tail_index = file.rfind('.')-4
	last_year = int(today.strftime('%Y'))-1
	last_year_output_file = f'{output_file[:no_tail_index]}{last_year}.csv'
	return last_year_output_file
	
	
def get_last_entry(filename):
	last_years_file = gen_last_year_file(filename)
	with open(filename, 'r') as file:
		last_entry = file.readlines()[-1].strip().split(', ')
		if last_entry == entry_headers:
			return get_last_entry(last_years_file)
		else: 	
			for _ in last_entry:
				if type(last_entry.index(_)) != int:
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
				
			entry = dict(zip(entry_headers, last_entry))
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


def get_current_zipcode():
	print('Identifying location....')
	location.start_updates()
	time.sleep(3)
	loc = location.get_location()
	addr = location.reverse_geocode(loc)
	location.stop_updates()
	return addr[0].get('ZIP') #zipcode as str


def get_loc_from_zip(zipcode):
	if zipcode in loc_zips:
		loc = loc_zips.get(zipcode,)
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


def append_file(file, entry):
	print(f'Writing to {file}...')
	with open(file, 'a') as f:
		f.write(f"{entry['date']}, {entry['startloc']}, {entry['endloc']}, {entry['startodo']}, {entry['endodo']}, {entry['tripmiles']}\n")
		
		
def create_entry(entry):
	'''takes arg as list with 6 values in accordance with entry_headers and return dict with keys as entry headers and values as the 6 from arg'''
	trip = entry[1] + entry[2]
	try:
		if config.loc2loc_miles.get(trip) == None:
			raise NoTripFound
	except NoTripFound:
		print(f'Trip "{trip}" not found in _config.py. Exiting...')
		exit()
	new_entry = dict(zip(entry_headers, entry))
	return new_entry


def main():
	last_known_loc = set_last_known_loc()
	last_known_odo = set_last_known_odo()
	missed_reading = True
	entries = [get_last_entry(output_file)]
	if entries[-1] == ['date', ' startloc', ' endloc', ' startodo', ' endodo', ' tripmiles']:
		entries = [] #avoid having headers in entries calculations
	
	while missed_reading:
		last_entry = get_last_entry(output_file)
		start_loc = last_known_loc
		end_loc = ''
		
		if last_entry.get('date') != date and entries[-1].get('date') != date:
			
			if last_entry['endloc'] != 'LL':
				final = [last_entry['date'],
				last_entry['endloc'], 
				'LL',
				last_entry['endodo'],
				int(last_entry['endodo']) + get_loc2loc_miles(last_entry['endloc'], 'LL'),
				int(get_loc2loc_miles(last_entry['endloc'], home_loc))]
				
				final = create_entry(final)
				append_file(output_file, final)
				print(f'Missing final trip added to previous date.\n{final}\n')
				
			entries = [] #remove earlier than today entries
			entries.append(create_entry([date, 'HM', home_loc, 1, 1, get_loc2loc_miles('HM', home_loc)]))
			
		prior_entry = [entries[-1].get(item) for item in entries[-1]]
		print(f'LAST ENTRY: {prior_entry}')
		end_odo = set_odo()
			
		#get missing trip info and add to list of entries	
		if end_odo == 1: 
			end_loc = input('Location > ').strip().upper()
			start_loc = entries[-1].get('endloc')
			entries.append(create_entry([date, start_loc, end_loc, 1, end_odo, get_loc2loc_miles(start_loc, end_loc)]))
			continue
		else: #get current trip info and back-calculate mileage readings
			missed_reading = False
			start_loc = entries[-1]['endloc']
			end_loc = get_loc_from_zip(get_current_zipcode())
			#print(f'Zipcode: {end_loc}')
			
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
		
if __name__ == "__main__":
	main()
