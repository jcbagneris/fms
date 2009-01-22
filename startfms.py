#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Financial Market Simulator
"""

__author__ = "Jean-Charles Bagneris <jcb@bagneris.net>"
__license__ = "BSD"

import sys
import os.path
import logging

import fms
from fms.utils import XmlParamsParser, YamlParamsParser, close_files, delete_files


def main():
    """
    Run experiment :
    - parse command line options and arguments
    - read simulation config file
    - call constructors for
      - world
      - engines and markets
      - agents
    - run [command]
    """
    parser = fms.set_parser()
    options, arguments = parser.parse_args()

    version = fms.get_full_version()
    if options.version:
        print "FMS v%s" % version
        return 0

    loglevel = 'error'
    if options.verbose:
        loglevel = 'info'
    if options.loglevel:
        loggelevel = options.loglevel
    logger = fms.set_logger(loglevel)
    logger.info("This is FMS v%s" % version)

    try:
        command = arguments[0]
    except IndexError:
        parser.print_help()
        logger.critical("Missing command name.")
        return 2

    known_commands = ('run', 'check')
    if command not in known_commands:
        logger.critical("Unknown command: %s" % command)
        return 2

    try:
        simconffile = arguments[1]
    except IndexError:
        logger.critical("Missing simulation config file name.")
        return 2

    if os.path.splitext(simconffile)[-1] == '.xml':
        logger.debug("Calling XmlParamsParser on %s" % simconffile)
        params = XmlParamsParser(simconffile)
    else:
        logger.debug("Calling YamlParamsParser on %s" % simconffile)
        params = YamlParamsParser(simconffile)

    world = fms.set_world(params)
    engineslist = fms.set_engines(params)
    agentslist = fms.set_agents(params)
            
    if command == 'run':
        logger.info("All is set, running simulation")
        for e in engineslist:
            logger.info("Running %s" % e['instance'])
            e['instance'].run(world, agentslist, e['market']['instance'])
        logger.info("Done.")
        close_files(params)

    if command =='check':
        close_files(params)
        delete_files(params)

if __name__ == "__main__":
    sys.exit(main())
