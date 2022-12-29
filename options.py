'''options.py'''

from datetime import date
import functions as func
import types
import c_trips
import _config
TODAY = _config.TODAY

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
    '''defined per options set below'''
      

## setup individual options and assign execute function
opts = {}

# help
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


# exit
e = Option('e')

def exit_loop(self, *args):
  while True:
        j = input("Exit?(y/n)")
        if j == 'y':
          print('exiting...')
          exit()
        elif j == 'n':
          break
e.execute = types.MethodType(exit_loop, e)
e.helpertext = 'e - exit'
opts['e'] = e

# add manual entry
a = Option('a')


a.execute = types.MethodType(func.exec_a_loop, a)
a.helpertext = '''
a - Add entry manually using format:\nmm/dd/yy startloc endloc startodo endodo miles'''
opts['a'] = a

# add "smart" entry
s = Option('s')
def exec_s(self):
  last_entry = func.get_last_entry(_config.output_file)
  
  #generate entry items
  loc1 = func.loc1_generator(last_entry)
  loc2 = func.loc2_generator()
  mi = func.get_loc2loc_miles(loc1, loc2)
  odos = s_odo_generator(last_entry, mi)
  odo1 = odos[0]
  odo2 = odos[1]
  
  entry = [TODAY, loc1, loc2, odo1, odo2, mi]
  
  #check for prior entry "today"
  func.validate_entry(entry)
  entry = func.clean_manual_input(*entry)
  
  func.append_file(entry)
  

s.execute = types.MethodType(exec_s, s)
opts['s'] = s

def s_odo_generator(last_entry, mi):
  '''generation of odo readings for smart add option'''
  if last_entry.get('date') == _config.TODAY:
    odo1 = last_entry.get('odo2')
    odo2 = odo1 + mi
  else:
    odo2 = func.set_odo()
    odo1 = odo2 - mi
  return [odo1, odo2]
    
#add multiple entries
m = Option('m')
