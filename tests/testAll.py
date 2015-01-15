#! /bin/python
import logging
_log = logging.getLogger("testAll")
import unittest

if __name__ == '__main__':
    logging.basicConfig( level=logging.DEBUG )
    runner=unittest.TextTestRunner(verbosity=2, failfast=True)
    runner.run(unittest.TestLoader().discover('./'))
