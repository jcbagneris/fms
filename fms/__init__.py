#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
FMS core module.
"""

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
