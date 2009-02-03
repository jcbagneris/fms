#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Run all test modules in current directory.
"""

import os
import unittest
import doctest
import glob
import logging
from StringIO import StringIO

import fms
from fms.utils import YamlParamsParser

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

def expList():
    """
    Return list of experiments conffiles in fixtures/fulltest dir
    """
    return glob.glob("fixtures/fulltests/*.yml")


logger = fms.set_logger('info','fms-tests')

logger.info("Running unittests")
suite = unittest.TestSuite()

for modtestname in sourceList():
    exec "import %s" % modtestname
    modtest = globals()[modtestname]
    if hasattr(modtest, 'suite'):
        suite.addTest(modtest.suite())
    else:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(modtest))

for root, dir, files in os.walk(os.path.dirname(fms.__file__)):
    for f in files:
        if os.path.splitext(f)[1] == '.py':
            path = os.path.split(root)[1]
            if path == 'fms':
                suite.addTest(doctest.DocFileSuite(f, package='fms',
                    optionflags=+doctest.ELLIPSIS))
            else:
                suite.addTest(doctest.DocFileSuite(
                    os.path.join(os.path.split(root)[1], f),
                    package='fms',
                    optionflags=+doctest.ELLIPSIS))

unittest.TextTestRunner(verbosity=2).run(suite)

for simconffile in expList():
    logger.info("Running %s" % simconffile)
    params = YamlParamsParser(simconffile)
    params['showbooks'] = False
    params.outputfile = StringIO()
    (world, engineslist, agentslist) = fms.set_classes(params)
    for e in engineslist:
        e['instance'].run(world, agentslist, e['market']['instance'])
    benchfile = "%s.csv" % simconffile.split('.')[0]
    benchmark = open(benchfile).read()
    testresult = params.outputfile.getvalue()
    if not benchmark == testresult:
        logger.error("%s failed" % simconffile)
        print testresult
    else:
        logger.info("%s ok" % simconffile)
    params.close_files()
    agentslist[0].reset()
            

