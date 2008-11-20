#!/usr/bin/python
"""
A minimal and over simplistic world class
"""

from fms import worlds

class NullWorld(worlds.World):
    """
    Minimal world class, does not provide any information
    """
    def __init__(self, parameters=None):
        pass

    def state(self):
        """
        Nullworld does not return any information
        """
        return None

if __name__ == '__main__':
    print NullWorld()
