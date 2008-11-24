#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
World module.
"""

class World:
    """
    Abstract world class
    """

    def __init__(self):
        self.lastmarketinfo = {'sellbook':[], 'buybook':[]}
        self.time = 0

    def __str__(self):
        return "%s world %s" % (self.__class__, id(self))

    def state(self):
        """
        Return world current state, as dict.
        Should be implemented in subclass

        Note that world state should include at any time
        Market.info() of previous period, allowing for change
        of engine and market class during simulation without losing
        current state (order books, ...).
        """
        raise NotImplementedError

