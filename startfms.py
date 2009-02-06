#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Financial Market Simulator
"""

__author__ = "Jean-Charles Bagneris <jcb@bagneris.net>"
__license__ = "BSD"

import sys
import logging

import fms

def main():
    """
    Run experiment :
    - parse command line options and arguments
    - read simulation config file
    - run [command]
    """
    parser = fms.set_parser()
    options, arguments = parser.parse_args()
    logger = fms.set_logger(options)
    command = fms.get_command(arguments, parser)
    getattr(fms, "do_%s" % command)(arguments, options)
    return 0

if __name__ == "__main__":
    sys.exit(main())
