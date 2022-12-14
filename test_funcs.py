from unittest import TestCase, main
from unittest.mock import patch
import functions as func
import _config as conf


class Test_funcs(TestCase):
  
  valid_input="12/22/22 ll lw 100 118 18"
  
  def setUp(self):
    self.file = conf.test_output_file
    
  @patch('functions.input', return_value=valid_input)  
  def test_exec_a_loop(self, input):
    func.exec_a_loop()
  
if __name__ == "__main__":
  main()
