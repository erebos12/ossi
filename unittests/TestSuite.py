import sys
import unittest

loader = unittest.TestLoader()

tests = loader.discover('.')

#ret = not unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful()
#sys.exit(ret)
