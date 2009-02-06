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
            self.csvdelimiter = params['csvdelimiter']
            self.clearbooksateod = params['engines'][offset]['clearbooksateod']
            self.showbooks = params['show_books']
            self.unique_by_agent = params['unique_by_agent']
        else:
            self.days = 1
            self.daylength = 1
            self.csvdelimiter = ';'
            self.clearbooksateod = True
            self.showbooks = False
            self.unique_by_agent = True

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
        - call market.do_clearing when needed, in a 
          synchronous or asynchronous way.
        - call market.clear_books() at the end of any day if necessary
        """
        raise NotImplementedError

    def output_order(self, order):
        """
        Output an order in orderlogfile
        """
        mask = self.csvdelimiter.join(('%(direction)s',
            '%(price).2f','%(quantity)d','"%(agent)s"'))
        print >> self.params.orderslogfile, mask % order
