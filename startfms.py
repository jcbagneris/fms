#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Financial Market Simulator
"""

__author__ = "Jean-Charles Bagneris <jcb@bagneris.net>"
__license__ = "BSD"

import sys
import logging

import fms.core
from fms.core import set_parser, set_logger, get_command

def main():
    """
    Run experiment :
    - parse command line options and arguments
    - read simulation config file
    - run [command]
    """
    parser = set_parser()
    options, arguments = parser.parse_args()
    logger = set_logger(options)
    command = get_command(arguments, parser)
    getattr(fms.core, "do_%s" % command)(arguments, options)
    return 0

if __name__ == "__main__":
    sys.exit(main())
