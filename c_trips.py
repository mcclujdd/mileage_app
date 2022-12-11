from datetime import date
import re
import _config
import logging


class Trip:
  '''Trip entry consists of the date, the start location, end location, correspondent odometer readings, and miles traveled'''

  ENTRY_HEADERS = [
    'date', 'startloc', 'endloc', 'startodo', 'endodo', 'tripmiles'
  ]


  def __init__(self,
               date=date.today().strftime("%m/%d/%y"),
               output_file=_config.output_file):
    self.date = date
    self.output_file = output_file


  class ValidationError(BaseException):
    '''Failure to validate data format'''


  def validate_date(self, date):
    '''check date against regex to match mm/dd/yy'''
    d_expression = r"^([0][1-9]|[1][0-2])[\/]([0][1-9]|[1|2][0-9]|[3][0|1])[\/]([0-9]{2})$"
    result = bool(re.match(d_expression, date))
    if result == False:
      #logging.error('Date expression did not match regex.', date)
      return 'Invalid date format. Please use mm/dd/yy.'
    else:
      return


  def validate_loc(self, loc: str):
    if loc in _config.locations:
      return
    else:
      return f'Invalid location {loc}. Please reference config file "locations".'


  def validate_odo(self, startodo: int, endodo: int, tripmiles: int):
    if startodo < 1:
      return 'Invalid starting odometer. cannot be less than 1.'
    elif startodo < endodo and tripmiles == endodo - startodo:
      return
    else:
      actual = endodo-startodo
      return f'Invalid odometer reading. {endodo}-{startodo} is equal to {actual}, not {tripmiles}.'


  def validate_data(self, args: list) -> list:
    date = self.validate_date(args[0])
    loc1 = self.validate_loc(args[1])
    loc2 = self.validate_loc(args[2])
    odo = self.validate_odo(args[3], args[4], args[5])
    entry = [date, loc1, loc2, odo]
    errors =[]
    for _ in entry:
      if _ is not None and type(_) is str:
        errors.append(_)
    return errors


  def clean_manual_input(self, *args) -> dict:
    output = []
    headers = self.ENTRY_HEADERS

    for a in range(3):
      try:
        output.append(str(args[a + 1]))
      except ValueError as ve:
        print(ve)
        raise ValueError()

      except IndexError as ie:
        print('Input requires 6 arguments. Please try again.')
        raise IndexError

    for a in range(3):
      try:
        #check odometers to read   a<b and c=b-c
        output.append(int(args[a + 4]))
      except ValueError as ve:
        raise ValueError(f'{ve}: Please check values for accurate formatting.')

      except IndexError as ie:
        print('Input requires 6 arguments. Please try again.')

    output = dict(zip(headers, output))

    return output

  def new_manual_entry(self,
                       date: str,
                       start_loc: str,
                       end_loc: str,
                       start_odo: int,
                       end_odo: int,
                       miles: int) -> list:
    output = [date, start_loc, end_loc, start_odo, end_odo, miles]

    return output

  def get_last_entry(self, filename, headers=ENTRY_HEADERS):
    #   last_years_file = gen_last_year_file(filename)
    with open(filename, 'r') as file:
      last_entry = file.readlines()[-1].strip().split(', ')

      for _ in last_entry:
        if last_entry.index(_) > 2:
          try:
            last_entry[last_entry.index(_)] = int(_)
          except:
            print(
              f'Error with format of {output_file}. Make sure the last three values are whole numbers (integers).'
            )
            print('Exiting...')
            exit()
      try:
        if len(last_entry) != 6:
          raise NoTripFound
      except NoTripFound:
        print(
          f"ERROR: NoTripFound for last entry, check {output_file} formatting for 6 items. e.g.:\n1/1/70, AA, BB, 2000, 2100, 100"
        )
        exit()

      entry = dict(zip(headers, last_entry))
      return entry

  def append_file(self, entry: dict, file: str):
    print(f'Writing to {file}...')
    with open(file, 'a') as f:
      f.write(
        f"{entry['date']}, {entry['startloc']}, {entry['endloc']}, {entry['startodo']}, {entry['endodo']}, {entry['tripmiles']}\n"
      )

#x = Trip()
#x.validate_data(["08/22/22", 'LL', 'LW', 100, 118, 18]) #works
