#mileage config.py

# where to output trip info to
output_file = 'output.txt'

# uncomment for testing
#output_file = 'testing.txt'

DEBUG = False

#locations are unique 2 letter abbreviations. This dict is those 2 abbreviations combined.
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
	'HMLL': 37,
	'HMHM': 0
}

#zipcodes for automatic location detection
loc_zips = {
	'01950': 'AJ',
	'01841': 'LW',
	'01420': 'HM'
	}
