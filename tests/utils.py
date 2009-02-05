#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Tests for utils module.
"""

import unittest
import sys
from StringIO import StringIO
from fms.utils import YamlParamsParser, XmlParamsParser, CSVDELIMITERS
from fms.utils.exceptions import MissingParameter

class YamlParserTests(unittest.TestCase):
    """
    Tests for YamlParser class
    """
    def setUp(self):
        self.fixturesdir = "fixtures"

    def testExperimentNameDefaultValue(self):
        """
        Experiment name is built from filename if missing
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['name'], '%s/minimalconfig.yml experiment' % 
                                                self.fixturesdir)

    def testExperimentNameValue(self):
        """
        Experiment name is correctly read
        """
        ymlparamsfile = '%s/fullconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['name'], 'Test Experiment')

    def testUniqueByAgentDefaultValue(self):
        """
        unique_by_agent value is True if missing
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertTrue(params['unique_by_agent'])

    def testCsvDelimiterDefaultValue(self):
        """
        csvdelimiter value is ';' if missing
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['csvdelimiter'], ';')

    def testRandomseedDefaultValue(self):
        """
        Randomseed should be None if missing
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['randomseed'], None)

    def testRandomSeedValue(self):
        """
        Randomseed is read correctly
        """
        ymlparamsfile = '%s/fullconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['randomseed'], 12345678)

    def testOutputfileDefaultValue(self):
        """
        Outputfile should be sys.stdout if missing
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['outputfilename'], 'sys.stdout')

    def testOuputfileValue(self):
        """
        Outputfile might be read from config
        """
        ymlparamsfile = '%s/fullconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['outputfilename'], 
                '%s/dummyoutput.csv' % self.fixturesdir)

    def testOrdersLogFileDefaultValue(self):
        """
        OrdersLogFile shoud be None if missing
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['orderslogfilename'], None)

    def testOrderLogFileValue(self):
        """
        OrdersLogFile might be read from config
        """
        ymlparamsfile = '%s/fullconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['orderslogfilename'], 
            '%s/dummyoutput.log' % self.fixturesdir)

    def testWorldMandatory(self):
        """
        World param is mandatory in config file
        """
        ymlparamsfile = '%s/missingworld.yml' % self.fixturesdir
        self.assertRaises(MissingParameter, YamlParamsParser, 
                ymlparamsfile)

    def testWorldClassValue(self):
        """
        World class is read correctly
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['world']['classname'], 'NullWorld')

    def testOneEngineMandatory(self):
        """
        At least one engine param is mandatory in config file
        """
        ymlparamsfile = '%s/missingengine.yml' % self.fixturesdir
        self.assertRaises(MissingParameter, YamlParamsParser, 
                ymlparamsfile)

    def testEngineClassValue(self):
        """
        Engine classname is read correctly
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['engines'][0]['classname'], 
                'AsynchronousRandWReplace')

    def testDaysDefaultValue(self):
        """
        Engine's days param should be 1 if missing
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['engines'][0]['days'], 1)

    def testDaysValue(self):
        """
        Engine's days param is correctly read as an int
        """
        ymlparamsfile = '%s/fullconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['engines'][0]['days'], 2)

    def testClearBooksAtEODDefaultValue(self):
        """
        Clear books at end of day if this param is missing
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertTrue(params['engines'][0]['clearbooksateod'])

    def testClearBooksAtEODValue(self):
        """
        Engine's clearbooksateod param is correctly read
        """
        ymlparamsfile = '%s/fullconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertFalse(params['engines'][0]['clearbooksateod'])

    def testDaylengthDefaultValue(self):
        """
        Daylength should be 1 if missing
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['engines'][0]['daylength'], 1)

    def testDaylengthValue(self):
        """
        Daylength is correctly read as an int
        """
        ymlparamsfile = '%s/fullconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['engines'][0]['daylength'], 10)

    def testMarketMandatory(self):
        """
        One market param per engine is mandatory
        """
        ymlparamsfile = '%s/missingmarket.yml' % self.fixturesdir
        self.assertRaises(MissingParameter, YamlParamsParser, 
                ymlparamsfile)

    def testMarketClassValue(self):
        """
        Market param classname is read correctly
        """
        ymlparamsfile = '%s/minimalconfig.yml' % self.fixturesdir
        params = YamlParamsParser(ymlparamsfile)
        self.assertEqual(params['engines'][0]['market']['classname'], 
                'ContinuousOrderDriven')

    def testAgentsMandatory(self):
        """
        Agents param is mandatory in config file
        """
        ymlparamsfile = '%s/missingagents.yml' % self.fixturesdir
        self.assertRaises(MissingParameter, YamlParamsParser, 
                ymlparamsfile)

    def testAgentMandatory(self):
        """
        At least one agent param is mandatory in agents
        """
        ymlparamsfile = '%s/missingagent.yml' % self.fixturesdir
        self.assertRaises(MissingParameter, YamlParamsParser, 
                ymlparamsfile)

class XmlParserTests(unittest.TestCase):
    """
    Tests for XmlParser class
    """
    def setUp(self):
        self.fixturesdir = "fixtures"
        self.missingengine = """
        <experiments>
          <experiment>
            <world>
                <className>NullWorld</className>
            </world>
            <market>
                <className>DummyMarket</className>
            </market>
            <agents>
                <agent>
                    <className>StupidTrader</className>
                </agent>
            </agents>    
          </experiment>
        </experiments>
        """
        self.missingworld = """
        <experiments>
          <experiment>
            <simulationEngine>
                <className>AsynchronousRandom</className>
            </simulationEngine>
            <market>
                <className>DummyMarket</className>
            </market>
            <agents>
                <agent>
                    <className>StupidTrader</className>
                </agent>
            </agents>    
          </experiment>
        </experiments>
        """
        self.missingmarket = """
        <experiments>
          <experiment>
            <simulationEngine>
                <className>AsynchronousRandom</className>
            </simulationEngine>
            <world>
                <className>NullWorld</className>
            </world>
            <agents>
                <agent>
                    <className>StupidTrader</className>
                </agent>
            </agents>    
          </experiment>
        </experiments>
        """
        self.missingagents = """
        <experiments>
          <experiment>
            <simulationEngine>
                <className>AsynchronousRandom</className>
            </simulationEngine>
            <world>
                <className>NullWorld</className>
            </world>
            <market>
                <className>DummyMarket</className>
            </market>
          </experiment>
        </experiments>
        """
        self.missingagent = """
        <experiments>
          <experiment>
            <simulationEngine>
                <className>AsynchronousRandom</className>
            </simulationEngine>
            <world>
                <className>NullWorld</className>
            </world>
            <market>
                <className>DummyMarket</className>
            </market>
            <agents>
            </agents>    
          </experiment>
        </experiments>
        """

    def testExperimentNameDefaultValue(self):
        """
        Experiment name is built from filename if missing
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['name'], '%s/minimalconfig.xml experiment' % 
                                                self.fixturesdir)

    def testExperimentNameValue(self):
        """
        Experiment name is correctly read
        """
        xmlparamsfile = '%s/fullconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['name'], 'Test Experiment')

    def testRandomseedDefaultValue(self):
        """
        Randomseed should be None if missing
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['randomseed'], None)

    def testRandomSeedValue(self):
        """
        Randomseed is read correctly
        """
        xmlparamsfile = '%s/fullconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['randomseed'], '12345678')

    def testOutputfileDefaultValue(self):
        """
        Outputfile should be sys.stdout if missing
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['outputfilename'], 'sys.stdout')

    def testOuputfileValue(self):
        """
        Outputfile might be read from config
        """
        xmlparamsfile = '%s/fullconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['outputfilename'], 
                '%s/dummyoutput.csv' % self.fixturesdir)

    def testOrdersLogFileDefaultValue(self):
        """
        OrdersLogFile shoud be None if missing
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['orderslogfilename'], None)

    def testOrderLogFileValue(self):
        """
        OrdersLogFile might be read from config
        """
        xmlparamsfile = '%s/fullconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['orderslogfilename'],
                '%s/dummyoutput.log' % self.fixturesdir)

    def testWorldMandatory(self):
        """
        World param is mandatory in config file
        """
        xmlparamsfile = StringIO(self.missingworld)
        self.assertRaises(MissingParameter, XmlParamsParser, 
                xmlparamsfile)

    def testWorldClassValue(self):
        """
        World class is read correctly
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['world']['classname'], 'NullWorld')

    def testOneEngineMandatory(self):
        """
        At least one engine param is mandatory in config file
        """
        xmlparamsfile = StringIO(self.missingengine)
        self.assertRaises(MissingParameter, XmlParamsParser, 
                xmlparamsfile)

    def testEngineClassValue(self):
        """
        Engine classname is read correctly
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['engines'][0]['classname'], 
                'AsynchronousRandom')

    def testDaysDefaultValue(self):
        """
        Engine's days param should be 1 if missing
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['engines'][0]['days'], 1)

    def testDaysValue(self):
        """
        Engine's days param is correctly read as an int
        """
        xmlparamsfile = '%s/fullconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['engines'][0]['days'], 2)

    def testClearBooksAtEODDefaultValue(self):
        """
        Engines clear books at end of day
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertTrue(params['engines'][0]['clearbooksateod'])

    def testDaylengthDefaultValue(self):
        """
        Daylength should be 1 if missing
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['engines'][0]['daylength'], 1)

    def testDaylengthValue(self):
        """
        Daylength is correctly read as an int
        """
        xmlparamsfile = '%s/fullconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['engines'][0]['daylength'], 10)

    def testMarketMandatory(self):
        """
        One market param per engine is mandatory
        """
        xmlparamsfile = StringIO(self.missingmarket)
        self.assertRaises(MissingParameter, XmlParamsParser, xmlparamsfile)

    def testMarketClassValue(self):
        """
        Market param classname is read correctly
        """
        xmlparamsfile = '%s/minimalconfig.xml' % self.fixturesdir
        params = XmlParamsParser(xmlparamsfile)
        self.assertEqual(params['engines'][0]['market']['classname'],
                'DummyMarket')

    def testAgentsMandatory(self):
        """
        Agents param is mandatory in config file
        """
        xmlparamsfile = StringIO(self.missingagents)
        self.assertRaises(MissingParameter, XmlParamsParser, xmlparamsfile)

    def testAgentMandatory(self):
        """
        At least one agent param is mandatory in agents
        """
        xmlparamsfile = StringIO(self.missingagent)
        self.assertRaises(MissingParameter, XmlParamsParser, xmlparamsfile)

if __name__ == "__main__":
    unittest.main()
