#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module defining SmartMem5TraderD agent class.
"""

import random

from fms import agents
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter

class SmartMem5TraderD(agents.Agent):
    """
    Simulate an agent taking decisions
    bounded by previous success.

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

    The SmartMem5TraderD acts by returning a
    dict with (direction, price, quantity) keys.
    Price is randomly chosen,
    in uniform distribution bounded by the previous
    five successes and all bids.
    It tries to maximize buy and sell quantities and
    chooses buy or sell based on projected wealth.
    It defects by a random amount.
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
        self.mem = 5
        # Prices of previous self.mem successfull bids
        self.successes = list()
        # All bids
        self.bids = list()

    def act(self, world=None, market=None):
        """
        Return order as a dict with keys in (direction, price, quantity).
        If SELL, pick price between highest success, next highest bid.
        If BUY, pick price between lowest success, next lowest bid.

        Avoid short selling and levering up (borrowing).
        """
        shift = int(random.random() * self.maxprice * 10)/100.
        if self.successes:
            # Average price of successful bids
            stockprice = float(sum(self.successes))/len(self.successes)
        else:
            stockprice = random.randint(1, self.maxprice*100)/100.

        try:
            minp = max(self.successes)
        except ValueError:
            # No successes
            minp = 0.01
        try:
            maxp = min([bid for bid in self.bids if bid > minp])
        except:
            # No higher bids
            maxp = self.maxprice
        sellprice = random.randint(int(minp*100), int(maxp*100))/100.
        sellquant = self.stocks
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
        buyprice = random.randint(int(minp*100), int(maxp*100))/100.
        if buyprice <= 0:
            buyprice = 0.01
        buyquant = int(self.money/buyprice)

        # Choose buy or sell, place order
        # Wealth if trader sells all his stock
        sellwealth = self.money + sellquant*sellprice
        # Wealth if trader uses as much money as possible to buy
        buywealth = self.money - buyquant*buyprice + \
                    (self.stocks + buyquant)*stockprice
        if sellwealth > buywealth:
            direction = SELL
            price = sellprice + shift
            quantity = sellquant
        else:
            direction = BUY
            price = buyprice - shift
            quantity = buyquant
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
