#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module defining SmartProbeBoundedTrader agent class.
"""
# Author: Patrick Coleman (Wharton Undergraduate 2012)

import random

from fms import agents
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter

class SmartProbeBoundedTrader(agents.Agent):
    """
    Simulate an agent probing and adjusting while
    not moving beyond reservation prices.

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

    The SmartProbeBoundedTrader acts by returning a
    dict with (direction, price, quantity) keys.
    It probes and adjusts below a buy reservation price
    and above a sell reservation price.
    Chooses buy or sell to maximize wealth and maximizes quantities.
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
        # {BUY: [prevprice, success], SELL: [prevprice, sucess]}
        self.prevorder = {BUY: [0.01, False], SELL: [self.maxprice, False]}
        # Reservation prices
        self.resbuy = random.randint(1, int(self.maxprice*50))/100.
        self.ressell = random.randint(int(self.maxprice*50), \
                                          self.maxprice*100)/100.
        # Successful bids
        self.successes = list()

    def act(self, world=None, market=None):
        """
        Return order as a dict with keys in (direction, price, quantity).
        If BUY, bid lower if last order was successful, otherwise higher.
        If SELL, bid higher if last order was successful, otherwise lower.
        Bids are random bounded by previous bid and reservation prices.

        To avoid short selling as far as possible, if # of stocks
        is zero or negative, force BUY direction.

        To avoid levering up as far as possible, if money
        is zero or negative, force SELL.
        """
        if self.successes:
            # Average price of successful bids
            stockprice = float(sum(self.successes))/len(self.successes)
        else:
            stockprice = random.randint(1, self.maxprice*100)/100.

        if self.prevorder[SELL][1]:
            sellprice = random.randint(int(self.prevorder[SELL][0]*100), \
                        self.maxprice*100)/100.
        else:
            sellprice = random.randint(int(self.ressell*100-1), \
                        int(self.prevorder[SELL][0]*100+1))/100.
        sellquant = self.stocks
        if self.prevorder[BUY][1]:
            buyprice = random.randint(1, \
                       int(self.prevorder[BUY][0]*100))/100.
        else:
            buyprice = random.randint(int(self.prevorder[BUY][0]*100-1), \
                       int(self.resbuy*100+1))/100.
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
            price = sellprice
            quantity = sellquant
        else:
            direction = BUY
            price = buyprice
            quantity = buyquant
        self.prevorder[direction] = [price, False]
        return {'direction':direction, 'price':price, 'quantity':quantity}

    def record(self, direction, price, quantity):
        """
        Record transaction
        """
        if direction:
            self.stocks -= quantity
            self.money += quantity*price
            self.prevorder[SELL] = [price, True]
        else:
            self.stocks += quantity
            self.money -= quantity*price
            self.prevorder[BUY] = [price, True]
        self.successes.append(price)


def _test():
    """
    Run tests in docstrings
    """
    import doctest
    doctest.testmod(optionflags=+doctest.ELLIPSIS)

if __name__ == '__main__':
    _test()
