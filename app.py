# take user input to help track mileage for import to google sheets mileage worksheet

# accomodate for forgetting location/odo readings: enter while loop to ask for odo and grab auto location. break out if odo value is NOT 1. if it is one, DONT run the auto lcoatiok function, instead ask for location.

#todo: add a verification for when manual entry odo doesnt match the value for trip_miles

from datetime import date
import location
import time


loc_zips = {
	'01950': 'AJ',
	'01841': 'LW',
	'01420': 'HM'
}
loc2loc_miles = {
	'AJLL': 37,
	'AJLS': 32,
	'AJLW': 21,
	'LLAJ': 38,
	'LLLS': 3,
	'LLLW': 18,
	'LLHM': 35,
	'LSAJ': 32,
	'LSLL': 3,
	'LSLW': 13,
	'LWAJ': 21,
	'LWLL': 17,
	'LWLS': 12,
	'HMLL': 37
	}
today = date.today()
date = today.strftime("%m/%d/%y")
data= ()


def set_last_known_loc():
	with open('output.txt', 'r') as file:
		f = file.readlines()[-1].split(',')
		if f[0] == date:
			return f[2].strip()
		else:
			return 'HM'
			
def set_last_known_odo():
	with open('output.txt', 'r') as file:
		f = file.readlines()[-1].split(',')
		try:
			odo = int(f[4].strip())
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


#todo: add function to convert location to key value as per locations dict
def zip2loc(zipcode):
	return loc_zips.get(zipcode)


def calculate_missing_odo(first, second, loc1,loc2):
	trip_mi = loc1+loc2 
	if first == 1:
		first = second - loc2loc_miles.get(trip_mi)
		return first
	elif second == 1:
		second = first + loc2loc_miles.get(trip_mi)
		return  second
		

def main_loop():
	last_known_loc = set_last_known_loc()
	last_known_odo = set_last_known_odo()
	missed_reading = True

	while missed_reading:
		
		start_loc = last_known_loc #start loc
		#b = input('Start Location > ').strip().upper()
		end_loc = '' #end loc
		#end_loc = input('End Location > ').strip().upper()
		#start_odo = int(input('Start Odometer > '))
		end_odo = set_odo()
		
		#set location
		if end_odo == 1:
			end_loc = input('Location > ').strip().upper()
			data = (date, end_odo, end_loc)
		else: 
			missed_reading = False
			zipcode = set_loc()
			if zipcode in loc_zips:
				end_loc = loc_zips.get(zipcode)
			else:
				end_loc = input('Current Location > ').strip().upper()
				
		#set start_odo
		start_odo = last_known_odo
		trip = start_loc+end_loc
		trip_mi = loc2loc_miles.get(trip)
		if end_odo == 1:
			end_odo = start_odo+trip_mi
		else:
			pass
		
		
		
		
		
		
		print(f'date={date}, start_loc={start_loc}, end_loc={end_loc}, start_odo={start_odo}, end_odo={end_odo}, trip_mi = {trip_mi}')
		
		print('Writing to output.txt...')
		try:
			with open('output.txt', 'a') as file:
				file.write(f'{date}, {start_loc}, {end_loc}, {start_odo}, {end_odo}, {trip_mi}\n')
				print('Done.')
		except:
			print('Failed.')
		
		#for use if not writing to file
		last_known_loc = end_loc
		last_known_odo = end_odo
		start_odo = last_known_odo
		
main_loop()
