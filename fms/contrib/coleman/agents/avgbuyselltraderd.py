#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module defining AvgBuySellTraderD agent class.
"""

import random

from fms import agents
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter

class AvgBuySellTraderD(agents.Agent):
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

    The AvgBuySellTraderD acts by returning a
    dict with (direction, price, quantity) keys.
    The 3 elements of the dict are randomly chosen,
    in uniform distributions at first. Leverage discouraged.
    As the agent acquires more information it will pick
    buy or sell based on relative attractiveness measured
    by wealth plus stock.
    Trader also defects by a random amount.
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
        # Successes
        self.sellhist = list()
        self.buyhist = list()
        # Bids
        self.buybids = list()
        self.sellbids = list()

    def act(self, world=None, market=None):
        """
        Return order as a dict with keys in (direction, price, quantity).
        Until trader gets data, use random prices.
        Evaluates attractiveness of buy vs sell.
        Buys or sells as much as it can.
        Pick price based on average of bids and successful bids,
        weighted more heavily to successes depending on number of
        successes (buy or sell depending on choice).

        Avoid short selling and levering up (borrowing).
        """
        shift = int(random.random() * self.maxprice * 10)/100.
        successes = self.sellhist + self.buyhist
        bids = self.sellbids + self.buybids
        sellprice = 0
        buyprice = 0
        if successes:
            # Average price of successful bids
            stockprice = float(sum(successes))/len(successes)
        else:
            stockprice = random.randint(1, self.maxprice*100)/100.
        if self.sellhist:
            # Average price of successful sells
            sellprice = float(sum(self.sellhist))/len(self.sellhist)
        if self.buyhist:
            # Average price of successful buys
            buyprice = float(sum(self.buyhist))/len(self.buyhist)
        if bids:
            # Average price of bids
            bidprice = float(sum(bids))/len(bids)
        else:
            bidprice = random.randint(1, self.maxprice*100)/100.

        # Set the buy or sell price as a weighted average of 
        # successful bid %  * avg successful price and
        # unsuccessful bid % * avg bid price for buy and sell.
        # Maximize buy and sell quantities.
        sellprice = sellprice * len(self.sellhist) + \
                    bidprice * (len(self.sellbids)-len(self.sellhist))
        try:
            sellprice = int(sellprice / len(self.sellbids) * 100)/100.
        except ZeroDivisionError:
            # No sell bids
            sellprice = random.randint(1, self.maxprice*100)/100.
        buyprice = buyprice * len(self.buyhist) + \
                   bidprice * (len(self.buybids)-len(self.buyhist))
        try:
            buyprice = int(buyprice / len(self.buybids) * 100)/100.
        except ZeroDivisionError:
            # No buy bids
            buyprice = random.randint(1, self.maxprice*100)/100.
        sellquant = self.stocks
        if buyprice == 0:
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
            self.sellbids.append(price)
        else:
            direction = BUY
            price = buyprice - shift
            quantity = buyquant
            self.buybids.append(price)
        return {'direction':direction, 'price':price, 'quantity':quantity}
        
    def record(self, direction, price, quantity):
        """
        Record transaction
        """
        if direction:
            self.stocks -= quantity
            self.money += quantity*price
            self.sellhist.append(price)
        else:
            self.stocks += quantity
            self.money -= quantity*price
            self.buyhist.append(price)

def _test():
    """
    Run tests in docstrings
    """
    import doctest
    doctest.testmod(optionflags=+doctest.ELLIPSIS)

if __name__ == '__main__':
    _test()
