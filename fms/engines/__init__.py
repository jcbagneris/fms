#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Engine module.
"""

class Engine:
    """
    Abstract simulation engine class
    """

    def __init__(self, params=None, offset=0):
        if params:
            self.days = params['engines'][offset]['days']
            self.daylength = params['engines'][offset]['daylength']
        else:
            self.days = 1
            self.daylength = 1

    def __str__(self):
        return "%s engine %s" % (self.__class__, id(self))

    def run(self, world, agents, market):
        """
        Run engine

        For days * daylength :
        - choose agent
        - let agent emit a desire (agent.act)
        - check desire validity (market.is_valid)
        - accumulate desire
        - market.record_order()
        - call market.doClearing when needed, in a 
          synchronous or asynchronous way.
        """
        raise NotImplementedError
