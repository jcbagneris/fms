#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
World module.
"""

import sys

class World:
    """
    Abstract world class
    """

    def __init__(self):
        self.lastmarketinfo = {'sellbook':[], 'buybook':[]}
        self.tick = 0
        self.day = 0

    def __str__(self):
        return "%s world %s" % (self.__class__, id(self))

    def show_time(self, day, time, max):
        """
        Print current tick on stderr
        """
        day += 1
        time += 1
        print >> sys.stderr, "%04d:%05d%s" % (day, time, "\b"*11),
        if day*time == max:
            print >> sys.stderr, "\n"

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

