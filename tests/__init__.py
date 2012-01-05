import os
import glob
import unittest
import importlib

here = os.path.dirname(__file__)

def test_all():
    suite = unittest.TestSuite()
    for fname in glob.glob(os.path.join(here, '*.py')):
        if '__init__' in fname:
            continue
        module = importlib.import_module('tests.' + os.path.basename(fname).split('.py')[0])
        suite.addTest(module.suite())
    return suite
