#!/usr/bin/env python
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
    def test_money_attribute_exists(self):
        """
        Agent should fail on __init__ if it does not have a money attribute
        """
        params = {'agents':[{'stocks':300}]}
        self.assertRaises(MissingParameter, Agent, params)

    def test_money_attribute_type(self):
        """
        Agent.money should be an int or a float
        """
        params = {'agents':[{'money':'blah', 'stocks':1000}]}
        self.assertRaises(ValueError, Agent, params)

    def test_stocks_attribute_exists(self):
        """
        Agent should fail on __init__ if it does not have a stocks attribute
        """
        params = {'agents':[{'money':1000}]}
        self.assertRaises(MissingParameter, Agent, params)

    def test_stocks_attribute_type(self):
        """
        Agent.stocks should be an int
        """
        params = {'agents':[{'money':200, 'stocks':23.4}]}
        self.assertRaises(NotAnInteger, Agent, params)
        params = {'agents':[{'money':200, 'stocks':'blah'}]}
        self.assertRaises(ValueError, Agent, params)

    def test_act_method_not_implemented(self):
        """
        Agent.act() method should be implemented in subclasses
        """
        params = {'agents':[{'money':200, 'stocks':15}]}
        smith = Agent(params)
        self.assertRaises(NotImplementedError, smith.act)

    def test_record_method(self):
        """
        Agent.record() should update Agent.money and Agent.stocks
        """
        params = {'agents':[{'stocks':300, 'money':600}]}
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
