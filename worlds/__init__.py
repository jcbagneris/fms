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
        pass

    def __str__(self):
        return "%s world %s" % (self.__class__, id(self))

    def state(self):
        """
        Return world current state, as dict.
        Should be implemented in subclass
        """
        raise NotImplementedError
