#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Tests for worlds module.
"""

import unittest
from fms.worlds import World

class WorldTests(unittest.TestCase):
    """
    Tests for Worlds abstract class
    """
    def test_state_method_is_implemented(self):
        """
        World.state() method should be implemented in subclasses
        """
        world = World()
        self.assertRaises(NotImplementedError, world.state)

if __name__ == "__main__":
    unittest.main()
