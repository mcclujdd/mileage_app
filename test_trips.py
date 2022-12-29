import unittest
import c_trips
import _config


class TestTrips(unittest.TestCase):
  def setUp(self):
    self.trip1 = c_trips.Trip()
    self.trip2 = c_trips.Trip("08/14/22")

  def test_date_is_str(self):
    self.date = self.trip1.date
    self.assertIsInstance(self.date, str)

  def test_date_manual_set(self):
    self.date = self.trip2.date
    self.assertEqual(self.date, "08/14/22",
                     "trip date is not set to manually indicate value.")

  def test_new_entry_returns_list(self):
    self.entry = c_trips.Trip().new_manual_entry("8/10/22", "LL", "LW", 100,
                                                 118, 18)
    self.assertIsInstance(self.entry, list)

  def test_validate_date_false(self):
    bad_dates = [
      '8/22/22', '0/07/22', '08-08-21', '08/08/2022', '02/7/22', '08/8/22'
    ]
    for d in bad_dates:
      r = self.trip1.validate_date(d)
      self.assertIsNotNone(r, f'{d} returned {r}')

  def test_validate_locations(self):
    bad_locs = ['h', 'aaa', '73', 'n']
    for loc in bad_locs:
      l = self.trip1.validate_loc(loc)
      self.assertIsNotNone(l, f'{loc} returned {l}')

  def test_validate_odo(self):
    good_odos = [[5, 9, 4], [100, 134, 34], [43222, 43454, 232]]
    bad_odos = [[4, 6, 1], [6, 2, 4], [-4, 5, 9]]
    for _ in good_odos:
      g = self.trip1.validate_odo(*_)
      self.assertIsNone(g)
    for _ in bad_odos:
      b = self.trip1.validate_odo(*_)
      self.assertIsNotNone(b)

  def test_validate_data_returns_errors(self):
    false_entry = ["08/8/22", "LL", "LW", 100, 118, 18]
    self.assertGreater(len(self.trip1.validate_data(false_entry)), 0)
    
    
  def test_validate_data_returns_none(self):
    true_entry = ["08/08/22", "LL", "LW", 100, 118, 18]
    x = self.trip1.validate_data(true_entry)
    self.assertEqual(len(x), 0)
    
    
if __name__ == "__main__":
  unittest.main()

