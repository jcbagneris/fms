#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module defining DefectorTrader agent class.
"""

import random

from fms import agents
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter

class DefectorTrader(agents.Agent):
    """
    Simulate an agent taking defecting from average decision

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

    The DefectorTrader acts by returning a
    dict with (direction, price, quantity) keys.
    Avg price is shifted up slightly for selling and down for buying. 
    Leverage discouraged.
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
        self.orders = list()

    def act(self, world=None, market=None):
        """
        Return shifted order as a dict with keys in (direction, price, quantity).

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
        shift = int(random.random() * self.maxprice * 10)/100.
        if len(self.orders) < 5:
            # Try some random bids before defecting
            price = random.randint(1, self.maxprice*100)/100.
        else:
            price = int(float(sum(self.orders))/len(self.orders)*100)/100.
        if direction:
            price += shift
            quantity = random.randint(1, self.stocks)
        else:
            price -= shift
            quantity = random.randint(1, self.maxbuy)
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
        self.orders.append(price)

def _test():
    """
    Run tests in docstrings
    """
    import doctest
    doctest.testmod(optionflags=+doctest.ELLIPSIS)

if __name__ == '__main__':
    _test()
