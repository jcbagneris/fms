#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Tests for agents module.
"""

import unittest
from fms.agents import Agent
from fms.utils.exceptions import MissingParameter, NotAnInteger

class AgentTests(unittest.TestCase):
    """
    Tests for Agent abstract class
    """
    def testMoneyAttributeExists(self):
        """
        Agent should fail on __init__ if it does not have a money attribute
        """
        params = {'stocks':300}
        self.assertRaises(MissingParameter, Agent, params)

    def testMoneyAttributeType(self):
        """
        Agent.money should be an int or a float
        """
        params = {'money':'blah', 'stocks':1000}
        self.assertRaises(ValueError, Agent, params)

    def testStocksAttributeExists(self):
        """
        Agent should fail on __init__ if it does not have a stocks attribute
        """
        params = {'money':1000}
        self.assertRaises(MissingParameter, Agent, params)

    def testStocksAttributeType(self):
        """
        Agent.stocks should be an int
        """
        params = {'money':200, 'stocks':23.4}
        self.assertRaises(NotAnInteger, Agent, params)
        params = {'money':200, 'stocks':'blah'}
        self.assertRaises(ValueError, Agent, params)

    def testActMethodNotImplemented(self):
        """
        Agent.act() method should be implemented in subclasses
        """
        params = {'money':200, 'stocks':15}
        smith = Agent(params)
        self.assertRaises(NotImplementedError, smith.act)

    def testRecordMethod(self):
        """
        Agent.record() should update Agent.money and Agent.stocks
        """
        params = {'stocks':300, 'money':600}
        smith = Agent(params)
        # smith buys 20 at 2.5
        smith.record(0, 2.5, 20)
        self.assertEqual(smith.stocks, 320,
                        "Agent.stocks incorrectly updated after buy")
        self.assertAlmostEqual(smith.money, 550., 2,
                        "Agent.money incorrectly updated after buy")
        # smith sells 30 à 3.2
        smith.record(1, 3.2, 30)
        self.assertEqual(smith.stocks, 290,
                        "Agent.stocks incorrectly updated after sell")
        self.assertAlmostEqual(smith.money, 646., 2,
                        "Agent.money incorrectly updated after sell")

if __name__ == "__main__":
    unittest.main()
