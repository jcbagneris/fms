#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Tests for markets module.
"""

import unittest
import sys
from fms.markets import Market
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter

class MarketTests(unittest.TestCase):
    """
    Tests for Market abstract class
    """
    def test_is_valid_not_implemented(self):
        """
        Market.is_valid() method should be implemented in subclasses
        """
        market = Market(None)
        self.assertRaises(NotImplementedError, market.is_valid, None, None)

    def test_info_not_implemented(self):
        """
        Market.info() method should be implemented in subclasses
        """
        class SubMarket(Market):
            """
            Dummy subclass for testing purpose
            """
            def __init__(self, parameters=None):
                Market.__init__(self, parameters)
        market = SubMarket(None)
        self.assertRaises(NotImplementedError, market.info)

    def test_output_file_default_value(self):
        """
        Outputfile default value is sys.stdout
        """
        market = Market(None)
        self.assertEqual(market.outputfile, sys.stdout)

    def test_sanitize_order_direction(self):
        """
        No direction in order shoud raise MissingParameter
        """
        market = Market(None)
        self.assertRaises(MissingParameter, market.sanitize_order, {'price':3})

    def test_sanitize_order_default_price(self):
        """
        If no price is given, price is best limit
        """
        market = Market(None)
        self.assertEqual(market.sanitize_order(
            {'direction':BUY})['price'], 'unset sellbook')
        self.assertEqual(market.sanitize_order(
            {'direction':SELL})['price'], 'unset buybook')

    def test_sanitize_order_price(self):
        """
        If price in raw order, use it
        """
        market = Market(None)
        self.assertAlmostEqual(market.sanitize_order(
            {'direction':SELL, 'price':3.85})['price'], 3.85, 2)

    def test_sanitize_order_default_quantity(self):
        """
        If no quantity is given, quantity is 1
        """
        market = Market(None)
        self.assertEqual(market.sanitize_order({'direction':BUY})['quantity'], 1)

    def test_sanitize_order_quantity(self):
        """
        If quantity in raw desire, use it
        """
        market = Market(None)
        self.assertEqual(market.sanitize_order(
            {'direction':SELL, 'quantity':200})['quantity'], 200)

if __name__ == "__main__":
    unittest.main()
