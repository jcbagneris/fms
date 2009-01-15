#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
FMS core module.
"""

import sys
import optparse

VERSION = '0.1.2'

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

