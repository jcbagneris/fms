#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Financial Market Simulator
"""

__author__ = "Jean-Charles Bagneris <jcb@bagneris.net>"
__license__ = "BSD"

import sys
import os.path
import optparse
import logging

from fms.utils import XmlParamsParser, YamlParamsParser

def set_parser():
    """
    Create command line arguments and options parser
    """
    optp = optparse.OptionParser(
        description='runs a Financial Market Simulator simulation',
        prog='%s' % sys.argv[0],
        usage="%prog [options] [command] simulationconffile",)
    optp.add_option('--version', action='store_true', 
        help="output FMS version and exit")
    optp.add_option('-v', '--verbose', action='store_true', 
        help="set logging level to 'info', overrided by --loglevel")
    optp.add_option('-L', '--loglevel', metavar='LEVEL', dest='loglevel',
        help="set logging level to LEVEL: debug, info, warning, error, critical")
    return optp

def set_logger(options):
    """
    Sets main logger instance.
    """
    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL,}

    logger = logging.getLogger('fms')
    lhandler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
    lhandler.setFormatter(formatter)
    logger.addHandler(lhandler)
    logger.setLevel(logging.ERROR)
    if options.verbose:
        logger.setLevel(logging.INFO)
    if options.loglevel:
        logger.setLevel(levels[options.loglevel])
    return logger

def import_class(modulename, classname):
    """
    Try to import classname from modulename.
    """
    logger = logging.getLogger('fms')
    try:
        exec "from %s import %s as themodule " % \
                (modulename, classname.lower())
    except ImportError:
        logger.critical("Unknown %s class: %s" % (modulename, classname))
        sys.exit(2)
    return themodule

def set_world(params):
    """
    Import world class and instanciate world
    """
    logger = logging.getLogger('fms')
    worldmodule = import_class('fms.worlds', params['world']['classname'])
    world = getattr(worldmodule, params['world']['classname'])(params)
    logger.info("Created world %s" % world)
    return world

def set_agents(params):
    """
    Import agents class and instanciate agents
    """
    logger = logging.getLogger('fms')
    agentslist = []
    for a in params['agents']:
        agentmodule = import_class('fms.agents', a['classname'])
        for i in range(a['number']):
            agentslist.append(getattr(agentmodule, a['classname'])(a))
        logger.info("Created  %d instances of agent %s" % 
                (a['number'], agentslist[-1].__class__))
    return agentslist

def set_engines(params):
    """
    Import engines and markets classes and instanciate them
    """
    logger = logging.getLogger('fms')
    engineslist = []
    for (offset, e) in enumerate(params['engines']):
        marketmodule = import_class('fms.markets', e['market']['classname'])
        e['market']['instance'] = getattr(marketmodule, 
                e['market']['classname'])(params)
        enginemodule = import_class('fms.engines', e['classname'])
        e['instance'] = getattr(enginemodule, e['classname'])(params, offset)
        engineslist.append(e)
        logger.info("Created engine-market  %s - %s" % 
                (e['instance'], e['market']['instance']))
    return engineslist


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
    parser = set_parser()
    options, arguments = parser.parse_args()

    if options.version:
        import fms
        print "FMS v%s" % fms.get_full_version()
        return 0

    logger = set_logger(options)

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

    world = set_world(params)
    engineslist = set_engines(params)
    agentslist = set_agents(params)
            
    if command == 'run':
        logger.info("All is set, running simulation")
        for e in engineslist:
            logger.info("Running %s" % e['instance'])
            e['instance'].run(world, agentslist, e['market']['instance'])
        logger.info("Done.")

if __name__ == "__main__":
    sys.exit(main())
