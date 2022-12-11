'''options.py'''

import functions as func
import types
import c_trips
import _config

class Option:
  '''simple option class'''


  def __init__(self, command):
    self.command = command
    self._helpertext = ""

  @property
  def helpertext(self): #getter
    return self._helpertext

  @helpertext.setter
  def helpertext(self, value):
    self._helpertext = value

  def execute(self, command: str, p1 = "") -> None:
    if self.command == 'e':
      print('exiting...')
      exit()
    elif self.command == 'a':
      pass


opts = {}

'''help option'''
h = Option('h')

def print_help_text(self, command = 'h') -> None:
  if command in opts:
    print(opts[command].helpertext)
  else:
    print(f'help for {command} not found')

h.execute = types.MethodType(print_help_text, h)
h.helpertext = '''
usage: [command]
      h - help 
      h [command] - show help for [command]
      e - exit
      a - add entry
      s - smart add
'''
opts['h'] = h


'''exit option'''
e = Option('e')

def exit_loop(self, *args):
  print('Exiting...')
  exit()
e.execute = types.MethodType(exit_loop, e)
e.helpertext = 'e - exit'
opts['e'] = e

'''add entry'''
a = Option('a')

def add_entry(self, entry: list, file=_config.output_file):
  #ensure uppercase locations
  try:
    assert len(entry) == 6
  except AssertionError:
    print('Invalid: Must input 6 values. h a for help.')
    return
  entry[1] = entry[1].upper()
  entry[2] = entry[2].upper()
  try:
    entry[3] = int(entry[3])
    entry[4] = int(entry[4])
    entry[5] = int(entry[5])
  except Exception as e:
    print('Invalid: Must use integers as final 3 values.')
    return 
  self.trip = c_trips.Trip()
  #new and testing
  errors = self.trip.validate_data(entry)
  try:
    assert len(errors) < 1
  except Exception as e:
    print('Validation Errors:\n')
    for err in errors: print(f'>>{err}')
    return
  
  ''' old and working---------v
  if not self.trip.validate_data(entry):
    print("invalid entry")
    return
  '''
  self.entry = self.trip.clean_manual_input(self, *entry)
  self.trip.append_file(self.entry, file)

a.execute = types.MethodType(add_entry, a)
a.helpertext = '''
a - Add entry manually using format:\nmm/dd/yy startloc endloc startodo endodo miles'''
opts['a'] = a


