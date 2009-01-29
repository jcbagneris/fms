#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module defining ZeroIntelligenceTrader agent class.
"""

import random

from fms import agents
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter

class ZeroIntelligenceTrader(agents.Agent):
    """
    Simulate an agent taking random decisions

    This agent subclass should have two keys in the
    args dict :
    - maxprice : maximum order price (float)
    - maxbuy : maximum quantity to buy (int)
    If any of those parameters is missing, a MissingParameter
    exception is raised.
    >>> from fms.agents import zerointelligencetrader
    >>> params = {'agents': [{'money':10000, 'stocks':200}]}
    >>> agent = zerointelligencetrader.ZeroIntelligenceTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: maxprice
    >>> params = {'agents': [{'money':10000, 'stocks':200, 'args':[999]}]}
    >>> agent = zerointelligencetrader.ZeroIntelligenceTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: maxbuy
    >>> params = {'agents': [{'money':10000, 'stocks':200, 'args':[999, 100]}]}
    >>> agent = zerointelligencetrader.ZeroIntelligenceTrader(params)
    >>> print agent.state()
    Agent ... - owns $10000.00 and    200 securities
    >>> print agent.maxprice
    999
    >>> print agent.maxbuy
    100

    The ZeroIntelligenceTrader acts by returning a
    dict with (direction, price, quantity) keys.
    The 3 elements of the dict are randomly chosen,
    in uniform distributions.
    >>> len(agent.act())
    3

    - direction is buy or sell
    - price is a %.2f float in [0.01,maxprice]
    - quantity is an int in :
      - if direction==BUY, [1,self.maxbuy]
      - if direction==SELL, [1,self.stocks]
    Thus, shortselling is not allowed.
    """
    
    def __init__(self, params, offset=0):
        agents.Agent.__init__(self, params, offset)
        try:
            self.maxprice = self.args[0]
        except (AttributeError, IndexError):
            raise MissingParameter, 'maxprice'
        try:
            self.maxbuy = self.args[1]
        except IndexError:
            raise MissingParameter, 'maxbuy'
        del self.args

    def act(self, world=None, market=None):
        """
        Return random order as a dict with keys in (direction, price, quantity).

        To avoid short selling as far as possible, if # of stocks
        is zero or negative, force BUY direction.
        """
        if self.stocks > 0:
            direction = random.choice((BUY, SELL))
        else:
            # stocks<=0, short selling is forbidden
            direction = BUY
        price = random.randint(1, self.maxprice*100)/100.
        if direction:
            quantity = random.randint(1, self.stocks)
        else:
            quantity = random.randint(1, self.maxbuy)
        return {'direction':direction, 'price':price, 'quantity':quantity}

def _test():
    """
    Run tests in docstrings
    """
    import doctest
    doctest.testmod(optionflags=+doctest.ELLIPSIS)

if __name__ == '__main__':
    _test()
