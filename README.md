Application for tracking mileage with very little user input.

*requires python 3.6 using pythonista for iOS*

# Basic Usage

Run mileage_2.0.py

Exit with e
Add entry with a
  data entry must follow specific formatting.
  *mm/dd/yy [2 letter start location] [2 letter end location] [starting odometer] [ending odometer]
  [total miles]*
Seek help with h
  h [command] for help with a specific command.

While at a destination, run the application with the mileage_2.0.py script.


# Configurations

The config.py file must have the following:

*output_file* set to desired output file name

*loc2loc_miles* as a dictionary with keys as concatenated locations and with values as integers for distance of the trip in miles. (e.g. 'AABB': 36)

*loc_zips* as a dictionary with keys as zip codes (type string) and with values as location abbreviations. (e.g. '98678': 'AA')

### Multiple locations for a single zip code need to be in list format e.g. '98678': ['AA', 'BB']

Optionals:

*name*: full name for final format filename (e.g. 'John Smith')

*cloud_path*: for file path to cloud storage file in pythonista (e.g. '/path_to_cloud/')
