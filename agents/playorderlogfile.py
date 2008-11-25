#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Module defining PlayOrderLogFile agent class.
"""

from fms import agents
from fms.utils.exceptions import MissingParameter

class PlayOrderLogFile(agents.Agent):
    """
    Agent taking decisions from an order file log.

    This agent subclass should have one item in the
    args list :
    - filename : the order logfile name (str)
    If this parameter is missing, a MissingParameter
    exception is raised.
    >>> params = {'money':10000, 'stocks':200}
    >>> agent = ZeroIntelligenceTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: orderlogfilename
    """
    
    def __init__(self, params):
        agents.Agent.__init__(self, params)
        try:
            filename = self.args[0]
        except (AttributeError, IndexError):
            raise MissingParameter, 'filename'
        del self.args
        self.logfile = open(filename, 'r')

    def act(self):
        """
        Return order as a dict with keys in (direction, price, quantity).

        Order is read from self.filename, one order (line) at a time.
        """
        line = '#'
        while line.startswith('#'):
            line = self.logfile.readline()
        direction, price, quantity = line.strip().split(';')
        direction = int(direction)
        price = float(price)
        quantity = int(quantity)
        return {'direction':direction, 'price':price, 'quantity':quantity}

def _test():
    """
    Run tests in docstrings
    """
    import doctest
    doctest.testmod(optionflags=+doctest.ELLIPSIS)

if __name__ == '__main__':
    _test()
