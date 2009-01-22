#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
FMS core module.
"""

import sys
import optparse
import logging

VERSION = '0.1.3a1'

def get_full_version():
    """
    Return full version number
    
    The full version includes last commit reference if any,
    i.e. if we run from a git repository.
    """
    from fms.utils import get_git_commit
    version = VERSION
    git_commit = get_git_commit()
    if git_commit:
        version = "%s-%s" % (version, git_commit)
    return version

def set_parser():
    """
    Create command line arguments and options parser
    """
    optp = optparse.OptionParser(
        description='run a Financial Market Simulator simulation',
        prog='%s' % sys.argv[0],
        usage="%prog [options] [command] simulationconffile",)
    optp.add_option('--version', action='store_true', 
        help="output FMS version and exit")
    optp.add_option('-v', '--verbose', action='store_true', 
        help="set logging level to 'info', overrided by --loglevel")
    optp.add_option('-L', '--loglevel', metavar='LEVEL', dest='loglevel',
        help="set logging level to LEVEL: debug, info, warning, error, critical")
    return optp

def set_logger(level, logname='fms'):
    """
    Sets main logger instance.
    """
    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL,}
    logger = logging.getLogger(logname)
    lhandler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
    lhandler.setFormatter(formatter)
    logger.addHandler(lhandler)
    logger.setLevel(levels[level])
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
    for (offset, a) in enumerate(params['agents']):
        agentmodule = import_class('fms.agents', a['classname'])
        for i in range(a['number']):
            agentslist.append(getattr(agentmodule, a['classname'])(params, offset))
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

