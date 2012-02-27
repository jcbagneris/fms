#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module defining Mem10Trader agent class.
"""

import random

from fms import agents
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter

class Mem10Trader(agents.Agent):
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

    The Mem10Trader acts by returning a
    dict with (direction, price, quantity) keys.
    The 3 elements of the dict are randomly chosen,
    in uniform distributions bounded by the previous
    ten successes and all bids.
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
        self.mem = 10
        # Prices of previous self.mem successfull bids
        self.successes = list()
        # All bids
        self.bids = list()

    def act(self, world=None, market=None):
        """
        Return order as a dict with keys in (direction, price, quantity).
        If SELL, pick price between highest success, next highest bid.
        If BUY, pick price between lowest success, next lowest bid.

        To avoid short selling as far as possible, if # of stocks
        is zero or negative, force BUY direction.
  
        To avoid levering up as far as possible, if money
        is zero or negative, force SELL.
        """
        if self.stocks > 0 and self.money > 0:
            direction = random.choice((BUY, SELL))
        elif self.stocks <= 0:
            # Short selling is forbidden
            direction = BUY
        else:
            # money<=0, levering is discouraged
            direction = SELL
        if direction:
            # SELL
            try:
                minp = max(self.successes)
            except ValueError:
                # No successes
                minp = 0.01 
            try:
                maxp = min([bid for bid in self.bids if bid > minp])
            except ValueError:
                # No higher bids
                maxp = self.maxprice
            quantity = random.randint(1, self.stocks)
        else:
            # BUY
            try:
                maxp = min(self.successes)
            except ValueError:
                # No successes
                maxp = self.maxprice
            try:
                minp = max([bid for bid in self.bids if bid < maxp])
            except ValueError:
                # No lower bids
                minp = 0.01
            quantity = random.randint(1, self.maxbuy)
        price = random.randint(int(minp*100), int(maxp*100))/100.
        self.bids.append(price)
        return {'direction':direction, 'price':price, 'quantity':quantity}

    def record(self, direction, price, quantity):
        """
        Record transaction
        """
        if direction:
            self.stocks -= quantity
            self.money += quantity*price
        else:
            self.stocks += quantity
            self.money -= quantity*price
        self.successes.append(price)
        if len(self.successes) > self.mem:
            self.successes.pop(0)


def _test():
    """
    Run tests in docstrings
    """
    import doctest
    doctest.testmod(optionflags=+doctest.ELLIPSIS)

if __name__ == '__main__':
    _test()
