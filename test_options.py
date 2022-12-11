import unittest
from options import opts
import functions
import _config

test_file = 'testing2022.csv'

class Test_options(unittest.TestCase):

  def test_help(self):
    h = opts['h'].helpertext
    self.assertIsInstance(h, str, 'should be a string')

  def test_exit(self):
    with self.assertRaises(SystemExit):
      opts['e'].execute()

  def test_add_entry_valid(self):
    entry = ["08/22/22", 'LL', 'LW', 100, 118, 18]
    #test for entry added to testing2022.csv
    opts['a'].execute(entry, test_file)
    last = list(functions.get_last_entry(test_file).values())
    self.assertEqual(entry, last)


  def test_add_entry_invalid_date(self):
    entry = ["11/7/22", "LL", "LW", 100, 118, 18]
    opts['a'].execute(entry, test_file)
    last = list(functions.get_last_entry(test_file).values())
    self.assertNotEqual(entry, last)


if __name__ == '__main__':
  unittest.main()

