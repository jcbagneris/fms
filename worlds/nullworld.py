#!/usr/bin/env python
"""
A minimal and over simplistic world class
"""

from fms import worlds

class NullWorld(worlds.World):
    """
    Minimal world class
    """
    def __init__(self, parameters=None):
        worlds.World.__init__(self)

    def state(self):
        """
        Nullworld only returns last market info (dict)
        """
        return self.lastmarketinfo

if __name__ == '__main__':
    print NullWorld()
