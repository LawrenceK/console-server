#! /bin/python
import sys
import logging
_log = logging.getLogger("testAll")
import unittest
sys.path.append( "../consoleserver")

if __name__ == '__main__':
    logging.basicConfig( level=logging.DEBUG )
    runner=unittest.TextTestRunner(verbosity=2, failfast=True)
    runner.run(unittest.TestLoader().discover('./'))
