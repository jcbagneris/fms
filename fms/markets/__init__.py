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
        self.replay = False
        if parameters:
            self.outputfile = parameters.outputfile
            self.csvdelimiter = parameters['csvdelimiter']
            if parameters['agents'][0]['classname'] == 'PlayOrderLogFile':
                self.replay = True
        else:
            self.outputfile = sys.stdout 
            self.csvdelimiter = ';'
        self.sellbook = []
        self.buybook = []

    def __str__(self):
        return "%s market %s" % (self.__class__, id(self))

    def is_valid(self, agent, desire):
        """
        Checks agent's desire validity
        
        Should be implemented in subclass.
        """
        raise NotImplementedError

    def clear_books(self):
        """
        Reset books to empty state
        """
        self.sellbook = []
        self.buybook = []

    def record_order(self, order, time, unique=True):
        """
        Record agent order in correct order book

        If an order from the same agent exists on the same
        asset and unique is True, delete it.

        >>> from fms.markets import Market
        >>> market = Market(None)
        >>> market.record_order({'direction': 1, 'quantity': 2, 'price': 3, 'agent': 'smith'}, 1)
        >>> market.sellbook
        [[3, 1, 2, 'smith']]
        >>> market.record_order({'direction': 1, 'quantity': 3, 'price': 4, 'agent': 'smith'}, 1)
        >>> market.sellbook
        [[4, 1, 3, 'smith']]
        >>> market.record_order({'direction': 1, 'quantity': 4, 'price': 5, 'agent': 'smith'}, 1, False)
        >>> market.sellbook
        [[4, 1, 3, 'smith'], [5, 1, 4, 'smith']]

        """
        if unique:
            for book in (self.sellbook, self.buybook):
                for line in book:
                    if order['agent'] == line[3]:
                        book.remove(line)
                        break
#            the for loop seems faster, probably because of the break
#            self.sellbook = filter((lambda x: order['agent'] != x[3]),
#                        self.sellbook)
#            self.buybook = filter((lambda x: order['agent'] != x[3]),
#                        self.buybook)

        if order['direction'] == SELL:
            self.sellbook.append(
                    [order['price'], time, order['quantity'], order['agent']])
            self.sellbook.sort()
        else:
            self.buybook.append(
                    [order['price'], -time, order['quantity'], order['agent']])
            self.buybook.sort()

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
            order['agent'] = raw_order['agent']
            return order
        else:
            raise MissingParameter, 'direction'

    def output_transaction(self, time, price, quantity):
        """
        Output a transaction line
        """
        mask = self.csvdelimiter.join(('%d','%d','%.2f','%d'))
        print >> self.outputfile, mask % (time,
                                        self.transaction,
                                        price, 
                                        quantity)


    def output_books(self, time):
        """
        Output best limits
        """
        sep = "-" * 39
        print sep
        print "          Sell orders at %03d" % time
        print "  Price | Quantity |     Emitter"
        for limit in self.sellbook[::-1][:5]:
            print " %6.2f | %8d | %s" % (limit[0], limit[2], limit[3])
        print sep
        for limit in self.buybook[::-1][:5]:
            print " %6.2f | %8d | %s" % (limit[0], limit[2], limit[3])
        print "  Price | Quantity |     Emitter"
        print "          Buy orders at %03d" % time
        print sep

