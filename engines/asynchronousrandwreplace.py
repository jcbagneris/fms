#!/usr/bin/env python
"""
Asynchronous random with replace engine
"""

import random

from fms.engines import Engine

class AsynchronousRandWReplace(Engine):
    """Asynchronous engine, random sampling of agents,
       with replacement.
    """

    def __init__(self, parameters=None, offset=0):
        """Constructor. Takes parameters from config.
           Seeds ramdom engine from parameter.randomseed, if any.
        """
        Engine.__init__(self, parameters, offset)
        self.params = parameters
        self.rank = offset
        if parameters:
            random.seed(parameters['randomseed'])

    def run(self, world, agents, market):
        """Sample agents (with replacement) and let them speak on market.
           As market is asynchronous, as soon as an agent speaks, doClearing
           is called to execute any possible transaction immediately.

           TODO: keep market state somewhere in order to chain multiple
           engines, possibly opening them with knowledge of previous one
           state (books, last transaction...)
        """
        market.sellbook = world.state()['sellbook']
        market.buybook = world.state()['buybook']
        transactions = market.info()['lasttransaction']
        while transactions < self.days*self.daylength: 
            agt = random.randint(0, len(agents)-1)
            order = agents[agt].act()
            valid = market.is_valid(agents[agt], order)
            if valid:
                if self.params.orderslogfile:
                    print >> self.params.orderslogfile, \
                            "%(direction)s;%(price).2f;%(quantity)d" % order
                market.record_order(agents[agt], order)
                market.do_clearing()
                transactions = market.info()['lasttransaction']
                world.lastmarketinfo.update(
                        {'sellbook':market.sellbook, 'buybook':market.buybook})

if __name__ == '__main__':
    print AsynchronousRandWReplace()
