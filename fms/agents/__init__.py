#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Agents module.
"""

from fms.utils.exceptions import MissingParameter, NotAnInteger

class Agent:
    """
    Abstract agent class.
    
    Any agent class inherits from agents.Agent, and should provide
    - a money attribute (float)
    - a stocks attribute (int)
    These attributes are passed in the parameters dict on instance 
    creation.

    Agent (sub)classes should provide an act() method,
    returning a tuple consisting of either :
    - (direction) : int, 0 buy, 1 sell
    - (direction, price) : price is a .2 float
    - (direction, price, quantity) : quantity is an int

    Agent class provides a record(direction,price,quantity) 
    method, returning nothing, and updating money and stocks
    of agent given the operation to record.
    """

    def __init__(self, params, offset=0):
        params = params['agents'][offset]
        for key in ('money', 'stocks'):
            if not key in params:
                raise MissingParameter, key
        for key in params:
            self.__dict__[key] = params[key]
        self.money = float(self.money)
        if '.' in str(self.stocks):
            raise NotAnInteger, self.stocks
        self.stocks = int(self.stocks)

    def __str__(self):
        return "<Agent %s>" % id(self)

    def state(self):
        return "Agent %s - owns $%8.2f and %6i securities" % (id(self), 
                self.money, self.stocks)

    def speak(self):
        """
        Return order emitted by agent
        """
        order = self.act()
        order['agent'] = order.get('agent', self)
        return order

    def act(self):
        """
        Emit an order on the market.
        Return order as dict, with following keys:
        - direction: BUY or SELL
        - price: float
        - quantity: int
        The only compulsory key is direction, others might
        be missing as markets are responsible to sanitize orders
        by calling Market.sanitize_order(order).
        Should be implemented in subclass.
        """
        raise NotImplementedError

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

