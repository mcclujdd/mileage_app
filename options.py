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
a.execute = types.MethodType(func.exec_a_loop, a)
a.helpertext = '''
a - Add entry manually using format:\nmm/dd/yy startloc endloc startodo endodo miles'''
opts['a'] = a


