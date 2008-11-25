#!/usr/bin/env python
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
    def test_run_method_is_implemented(self):
        """
        Engine.run() method should be implemented in subclasses
        """
        engine = Engine()
        self.assertRaises(NotImplementedError, engine.run, None, None, None)

if __name__ == "__main__":
    unittest.main()
