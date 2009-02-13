#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Order driven market, clearing is a "fixing".
Price is chosen to maximise transactions quantity.
Any order is considered valid.
"""

import logging

from fms import markets
from fms.utils import BUY, SELL

logger = logging.getLogger('fms.markets.highestqtyfixing')

class HighestQtyFixing(markets.Market):
    """
    Simulate an order driven market with end of period fixing.

    This market class uses 2 order books (buybook, sellbook).
    Books are sorted lists of [price, time, quantity, agent]
    to get the best limits for the next trade.
    As best limit is the highest offered price for buybook,
    and the lowest for sellbook, buybook[-1] and sellbook[0]
    are the best limits.
    Date is an int, the instant the order entered the book.
    Date is negative in buybook to ensure that buybook[-1]
    is always the best limit, i.e. if two orders have the same
    price limit, the older wins.

    The class inherits at least one parameter from its superclass,
    the file/device where transactions should be output. If no
    filename is given in conf file, then output goes to sys.stdout:
    >>> from fms.markets import highestqtyfixing
    >>> market = highestqtyfixing.HighestQtyFixing()
    >>> market.output_transaction(1, 10.0, 25)
    1;0;10.00;25

    Any agent can place any order : the market itself does not enforce
    any condition on the orders.
    >>> from fms import agents
    >>> agentbob = agents.Agent({'agents': [{'money':10000, 'stocks':200}]})
    >>> agentsmith = agents.Agent({'agents': [{'money':1000, 'stocks':2000}]})
    >>> order = (None,)
    >>> market.is_valid(agentbob, order)
    True
    >>> market.is_valid(agentsmith, order)
    True

    """

    def __init__(self, parameters=None):
        """
        Class constructor.
        Gets parameters from config, pass it to superclass.
        Adds :
        - lastprice (float) : last transaction price, see info()
        - transaction (int) : transaction counter
        """
        markets.Market.__init__(self, parameters)
        self.lastprice = None
        self.transaction = 0

    def is_valid(self, agent, order):
        """
        Checks if order is valid. Always True for this market.
        """
        return True

    def info(self):
        """
        Provides dict information about market state
        Dict keys :
        - selllimit (float): best sell limit
        - buylimit (float): best buy limit
        - lastprice (float): last transaction price
        - lasttransaction (int): # of last transaction
        """
        if self.sellbook:
            sellbook = self.sellbook
        else:
            sellbook = [['unset sellbook']]
        if self.buybook:
            buybook = self.buybook
        else:
            buybook = [['unset buybook']]
        infodict = {'sellbook': sellbook,
                    'buybook': buybook,
                    'lastprice': self.lastprice,
                    'lasttransaction': self.transaction}
        return infodict

    def do_clearing(self, fixingtime):
        """
        Clears books by 'fixing'.

        Choose fixing price which ensures the highest transactions
        volume.
        Execute all possible transactions at fixing price
        """
        fixdict = {}
        cumul = 0
        for price, time, qty, agent in reversed(self.buybook):
            cumul += qty
            fixdict.setdefault(price, [0,0])[0] = cumul
        cumul = 0
        for price, time, qty, agent in self.sellbook:
            cumul += qty
            fixdict.setdefault(price, [0,0])[1] = cumul
        fixingprice = max(
                ((min(i,j), price) for price, (i,j) in fixdict.items()))[1]
        logger.info("Fixing price is %.2f" % fixingprice)
        
        if len(self.buybook) and len(self.sellbook):
            while len(self.sellbook) and len(self.buybook) \
                    and self.sellbook[0][0] <= self.buybook[-1][0]:
                qty = min(self.buybook[-1][2], self.sellbook[0][2])
                executedprice = fixingprice
                self.lastprice = executedprice
                self.transaction += 1
                buyer = self.buybook[-1][3]
                seller = self.sellbook[0][3]
                if not self.replay:
                    buyer.record(BUY, executedprice, qty)
                    seller.record(SELL, executedprice, qty)
                self.output_transaction(fixingtime, executedprice, qty)
                if qty == self.buybook[-1][2]:
                    del self.buybook[-1]
                else:
                    self.buybook[-1][2] -= qty
                if qty == self.sellbook[0][2]:
                    del self.sellbook[0]
                else:
                    self.sellbook[0][2] -= qty


def _test():
    """
    Run tests in docstrings.
    """
    import doctest
    doctest.testmod(optionflags=+doctest.ELLIPSIS)

if __name__ == '__main__':
    _test()
