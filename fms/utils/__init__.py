#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Utilities modules

__init__.py only contains various constants to avoid mass imports from setup.py
"""

# Order directions
BUY = 0
SELL = 1

# csv delimiters
CSVDELIMITERS = [';', ',', '\t', ' ', ':', '|', '-', '!', '/']

# args
COMMANDS = ('nothing', 'run', 'check')
OPTS_VAL = ('outputfilename', 
        'orderslogfilename', 
        'randomseed', 
        'csvdelimiter', 
        'repeat')
OPTS_BOOL = {'show_books': False,
             'timer': False,
             'unique_by_agent': True,}

