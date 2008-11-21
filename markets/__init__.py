#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Market module.
"""

import sys
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter

class Market:
    """
    Abstract market class
    """

    def __init__(self, parameters):
        if parameters:
            self.outputfile = parameters.outputfile
        else:
            self.outputfile = sys.stdout 

    def __str__(self):
        return "%s market %s" % (self.__class__, id(self))

    def is_valid(self, agent, desire):
        """
        Checks agent's desire validity
        
        Should be implemented in subclass.
        """
        raise NotImplementedError

    def record_order(self, agent, order):
        """
        Records agent's order
        
        Should be implemented in subclass.
        """
        raise NotImplementedError

    def do_clearing(self):
        """
        Clears recorded desires
        
        Should be implemented in subclass.
        """
        raise NotImplementedError

    def info(self):
        """
        Returns market current state, as dict
        """
        if self.__class__.__name__ == 'Market':
            infodict = {'sellbook': [['unset sellbook']],
                        'buybook': [['unset buybook']],
                        'lasttransaction':0}
            return infodict
        else:
            raise NotImplementedError

    def sanitize_order(self, raw_order):
        """
        Returns agent's order as a dict with direction, price, quantity.
        raw_order should be a dict with at least 'direction' key.
        Order keys :
        - direction: BUY or SELL
        - price: best market limit if missing
        - quantity: 1 if missing
        """
        order = {}
        if 'direction' in raw_order:
            order['direction'] = raw_order['direction']
            if order['direction'] == BUY:
                order['price'] = raw_order.get('price', 
                        self.info()['sellbook'][0][0])
            else:
                order['price'] = raw_order.get('price', 
                        self.info()['buybook'][-1][0])
            order['quantity'] = raw_order.get('quantity', 1)
            return order
        else:
            raise MissingParameter, 'direction'

