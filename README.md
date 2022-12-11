Application for tracking mileage with very little user input.

*requires python 3.6 using pythonista for iOS*
*location services must be enabled for pythonista*

# BASIC

Run app.py. Enter odometer.


# MORE BETTER EXPLAINED

While at a destination, run the application with the app.py script.

Chronological trips for the day matter. If previous trips are needed, enter 1 for odometer and input the destination. Repeat until the destination is current and then input the current odometer.

If the location is not automatically detected with a current odometer reading, it will ask for a location.

If the trip is not in the configuration file (e.g Location AA to location BB as AABB) it will throw an exception and require an update to the config.py or a manual entry to the csv output file.


# CONFIGURATIONS

The config.py file must have the following:

*output_file* set to desired output file name

*loc2loc_miles* as a dictionary with keys as concatenated locations and with values as integers for distance of the trip in miles. (e.g. 'AABB': 36)

*loc_zips* as a dictionary with keys as zip codes (type string) and with values as location abbreviations. (e.g. '98678': 'AA')
# multiple locations for a single zip code need to be in list format e.g. '98678': ['AA', 'BB']

Optionals:

*name* full name for final format filename (e.g. 'John Smith')

*cloud_path* for file path to cloud storage file in pythonista (e.g. '/path_to_cloud/')

# CAUTION

It is important that the last location visited for the day is recorded. If not, the next time the app is run, it will take the last known location and add an entry from there to the home location assigned in the config file. This could result in errors or false trips and therefore incorrect mileage.
