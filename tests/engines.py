#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Tests for engines module.
"""

import unittest
from fms.engines import Engine

class EngineTests(unittest.TestCase):
    """
    Tests for Engine abstract class
    """
    def testRunMethodIsImplemented(self):
        """
        Engine.run() method should be implemented in subclasses
        """
        engine = Engine()
        self.assertRaises(NotImplementedError, engine.run, None, None, None)

if __name__ == "__main__":
    unittest.main()
