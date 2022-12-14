class NoTripFound(BaseException):
  '''failure to find a value for trip in the dictionary per the config file'''
  pass

class ValidationError(BaseException):
  '''Failure to validate data format'''
