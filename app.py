#mileage app.py
'''
take user input to help track mileage for import
 to google sheets mileage worksheet
'''
#todo: verify location isn't blank
import logging
import logging.config
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filename': 'mileage.log',
    'mode': 'a',
    'loggers': {
        '': {
            'level': 'DEBUG',
        },
        'another.module': {
            'level': 'DEBUG',
        },
    }
}
logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger(__name__)
logger.setLevel(10)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('mileage.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

from datetime import date
import location
import time

#load configurations
import config
output_file = config.output_file
loc2loc_miles = config.loc2loc_miles
loc_zips = config.loc_zips


today = date.today()
date = today.strftime("%m/%d/%y")
logger.info(f'date set as {date}')


def get_last_entry(filename):
	with open(filename, 'r') as file:
		result = file.readlines()[-1].strip().split(', ')
		for item in result:
			try:
				i = result.index(item)
				result[i] = int(item.strip())
			except:
				pass
	return result
	

def set_last_known_loc():
	f = get_last_entry(output_file)
	if f[0] == date:
		return f[2].strip()  #return end_loc
	else:
		return 'HM'


def set_last_known_odo():
	f = get_last_entry(output_file)
	try:
		odo = int(f[4])
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


def set_loc():
	print('Identifying location....')
	location.start_updates()
	time.sleep(5)
	loc = location.get_location()
	addr = location.reverse_geocode(loc)
	location.stop_updates()
	print('Done.')

	return addr[0].get('ZIP')
	

def append_file(file, data):
	print(f'Writing to {file}...')
	try:
		with open(file, 'a') as f:
			f.write(f'{data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}\n')
			print('Done.')
	except:
		print('Failed.')
		logger.error(f'Failed to write to {file}.')
		logger.debug(f'DATA: {data}')
		
def set_data(date, start_loc, end_loc, start_odo, end_odo, trip_mi):
	lst = [date, start_loc, end_loc, start_odo, end_odo, trip_mi]
	return lst
		

def zip2loc(zipcode):
	return loc_zips.get(zipcode)


def main_loop():
	last_known_loc = set_last_known_loc()
	last_known_odo = set_last_known_odo()
	missed_reading = True
	data = [get_last_entry(output_file)]
	if data[-1] == ['date', ' startloc', ' endloc', ' startodo', ' endodo', ' tripmiles']:
		data = []
	
	while missed_reading:
		
		
		last_entry = get_last_entry(output_file)
		print(data)
		start_loc = last_known_loc
		end_loc = ''
		
		if last_entry[0] != date and data[-1][0] != date:
			data = []
			data.append(set_data(date, 'HM', 'LL', 1, 1, loc2loc_miles.get('HMLL')))
			
			print(
			f'date={data[-1][0]}, start_loc={data[-1][1]}, end_loc={data[-1][2]}, start_odo={data[-1][3]}, end_odo={data[-1][4]}, trip_mi={data[-1][5]}')
			
		
		end_odo = set_odo()

		if end_odo == 1:
			end_loc = input('Location > ').strip().upper()
			start_loc = data[-1][2]
			data.append(set_data(date, start_loc, end_loc, 1, end_odo, loc2loc_miles.get(start_loc+end_loc)))
			continue
		else:
			missed_reading = False
			start_loc = data[-1][2]
			zipcode = set_loc()
			if zipcode in loc_zips:
				end_loc = loc_zips.get(zipcode)
			else:
				end_loc = input('Current Location > ').strip().upper()
			
				
			data.append(set_data(date, start_loc, end_loc, 1, end_odo, loc2loc_miles.get(start_loc+end_loc)))
			
			data.reverse()
			previous_end_odo = end_odo
			for lst in data:
				if lst[0] == date:
					lst[4] = int(previous_end_odo)
					lst[3] = lst[4] - lst[5]
					previous_end_odo = lst[3]
		
		data.reverse()
		for item in data:
			append_file(output_file, item)
		print(data)
		

main_loop()
