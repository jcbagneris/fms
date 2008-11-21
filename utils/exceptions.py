#!/usr/bin/env python
"""
FMS custom exceptions classes
"""
import logging

class MissingParameter(Exception):
    """
    Custom exception class for missing parameter in
    simulation config file.
    """
    def __init__(self, msg):
        logger = logging.getLogger("fms.utils.exceptions")
        logger.exception("Missing parameter: %s" % msg)
        self.msg = msg

    def __str__(self):
        return self.msg

class NotAnInteger(Exception):
    """
    Custom exception class: value should be an integer.
    """
    def __init__(self, value):
        logger = logging.getLogger("fms.utils.exceptions")
        logger.exception("Not an integer: %s" % value)
        self.value = value

    def __str__(self):
        return self.value
