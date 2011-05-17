#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
FMS core module.
"""

import sys
import os
import optparse
import logging

from fms.utils import XmlParamsParser, YamlParamsParser
from fms.utils import COMMANDS, OPTS_VAL, OPTS_BOOL

VERSION = '0.1.6'

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

def get_simconffile(args):
    """
    Get experiment config file name from command line
    """
    logger = logging.getLogger('fms')
    try:
        simconffile = args[1]
    except IndexError:
        logger.critical("Missing simulation config file name.")
        sys.exit(2)
    return simconffile

def apply_opts(params, opts):
    """
    Apply opts to params.

    Command line options override config file parameters
    """
    for opt in OPTS_VAL:
        optvalue = getattr(opts, opt)
        if optvalue:
            params[opt] = optvalue

    for opt in OPTS_BOOL:
        optvalue = getattr(opts, opt)
        if isinstance(optvalue, bool):
            params[opt] = optvalue
        else:
            if not opt in params:
                params[opt] = OPTS_BOOL[opt]

    if opts.repeat:
        for key in ('outputfilename', 'orderslogfilename'):
            if key in params:
                if params[key] not in ('None', 'sys.stdout'):
                    parts = params[key].rsplit('.',1)
                    params[key] = '.'.join((parts[0]+'-%03d', parts[1]))

    if opts.replay:
        del params['agents'][1:]
        if not params['agents'][0]['classname'] == 'PlayOrderLogFile':
            params['agents'][0]['classname'] = 'PlayOrderLogFile'
            params['agents'][0]['number'] = 1
            if not opts.orderslogfilename and not params['orderslogfilename']:
                params['orderslogfilename'] = '.'.join((
                        params['simconffile'].rsplit('.',1)[0],'log'))
            params['agents'][0]['args'] = [os.path.abspath(
                params['orderslogfilename'])]
            params['orderslogfilename'] = None

    if params['orderslogfilename'] in ('None', 'sys.stdout'):
        params['orderslogfilename'] = None

    return params

def get_params(args, opts):
    """
    Get params from conffile
    """
    logger = logging.getLogger('fms')
    simconffile = get_simconffile(args)
    if os.path.splitext(simconffile)[-1] == '.xml':
        logger.debug("Calling XmlParamsParser on %s" % simconffile)
        params = XmlParamsParser(simconffile)
    else:
        logger.debug("Calling YamlParamsParser on %s" % simconffile)
        params = YamlParamsParser(simconffile)
    params['simconffile'] = simconffile
    params = apply_opts(params, opts)
    params.printparams()
    return params

def get_command(args, parser):
    """
    Get command from command line arguments
    """
    logger = logging.getLogger('fms')
    try:
        command = args[0]
    except IndexError:
        parser.print_help()
        logger.critical("Missing command name.")
        sys.exit(2)
    if command not in COMMANDS:
        logger.critical("Unknown command: %s" % command)
        sys.exit(2)
    return command

def set_parser():
    """
    Create command line arguments and options parser
    """
    optp = optparse.OptionParser(
        description='run a Financial Market Simulator simulation',
        prog='%s' % sys.argv[0],
        usage="%prog [options] [command] simulationconffile",
        version = "This is FMS v%s" % get_full_version(),)
    # general value options
    optp.add_option('-L', '--loglevel', metavar='LEVEL', dest='loglevel',
        help="set logging level to LEVEL: debug, info, warning, error, critical")
    # boolean options overriding config parameters
    optp.add_option('-v', '--verbose', action='store_true',
        help="set logging level to 'info', overrided by --loglevel")
    optp.add_option('--show_books','--show_limits', action='store_true',
        dest="show_books", help="show best limits on each step")
    optp.add_option('-r', '--replay', action='store_true',
        help="Replay an orders logfile.")
    optp.add_option('-t', '--timer', action='store_true',
        help="Print a timer.")
    optp.add_option('--unique_by_agent', action='store_true',
        help="Only one order by agent in books.")
    optp.add_option('--no_unique_by_agent', action='store_false',
        dest='unique_by_agent',
        help="More than one order by agent allowed in books.")
    # value options overriding config parameters
    optp.add_option('--orderslogfilename', dest='orderslogfilename',
            help='orders log filename')
    optp.add_option('--outputfilename', '-o', dest='outputfilename',
            help='output filename')
    optp.add_option('--randomseed',
            help='random seed')
    optp.add_option('--csvdelimiter',
            help='csv delimiter')
    optp.add_option('--repeat',
            help='repeat experiment N times')

    return optp

def set_logger(options, logname='fms'):
    """
    Sets main logger instance.
    """
    if isinstance(options, str):
        loglevel = options
    else:
        loglevel = 'error'
        if options.verbose:
            loglevel = 'info'
        if options.loglevel:
            loglevel = options.loglevel
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
    logger.setLevel(levels[loglevel])
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

def set_classes(params):
    """
    Parse conffile and instanciate classes
    """
    world = set_world(params)
    engineslist = set_engines(params)
    agentslist = set_agents(params)
    return (world, engineslist, agentslist)
            
def do_check(args, opts):
    """
    Command: check experiment conffile, do not run
    """
    params = get_params(args, opts)
    for turn in xrange(int(params['repeat'])):
        (world, engineslist, agentslist) = set_classes(params)

def do_run(args, opts):
    """
    Command: run experiment
    """
    logger = logging.getLogger('fms')
    params = get_params(args, opts)
    if logger.getEffectiveLevel() < logging.INFO:
        params.showbooks = True
    for turn in xrange(int(params['repeat'])):
        params.create_files(turn)
        params.printfileheaders()
        (world, engineslist, agentslist) = set_classes(params)
        logger.info("All is set, running simulation %03d" % turn)
        for e in engineslist:
            logger.info("Running %s" % e['instance'])
            e['instance'].run(world, agentslist, e['market']['instance'])
        logger.info("Done.")
        params.close_files(turn)

