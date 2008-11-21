#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Run all test modules in current directory.
"""

import unittest
import glob

def sourceList():
    """
    Return list of all python modules except this one in current dir
    """
    liste = []
    for s in glob.glob("*.py"):
        if s == 'runalltests.py':
            continue
        s = s.split('.')[0]
        liste.append(s)
    return liste

suite = unittest.TestSuite()
for modtestname in sourceList():
    exec "import %s" % modtestname
    modtest = globals()[modtestname]
    if hasattr(modtest, 'suite'):
        suite.addTest(modtest.suite())
    else:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(modtest))

tests = unittest.TestSuite(suite)

unittest.TextTestRunner(verbosity=2).run(tests)
