#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
FMS version setting and getting.
"""

from fms.utils.git import get_git_commit_hash, get_git_status

TAG = '0.1.9'

def get_full_version():
    """
    Return full version number
    
    The full version includes last commit reference if any,
    i.e. if we run from a git repository.
    """
    from fms.utils.git import get_git_commit_hash, is_repo_clean, is_git_repo
    version = TAG
    if not is_git_repo():
        return version
    git_commit = get_git_commit_hash()[:8]
    if git_commit:
        version = "%s-%s" % (version, git_commit)
        if not is_repo_clean():
            version = "%s-dirty" % version
    return version

def get_version():
    """
    Return current version number.
    Version number is :
    - last tag number if last commit == last tag and repo is clean 
      or not a git repo (regular fms install)
    - get_full_version() otherwise
    """
    from fms.utils.git import get_git_commit_hash, is_git_repo, is_repo_clean
    if is_git_repo():
        if is_repo_clean():
            if get_git_commit_hash() == get_git_commit_hash(TAG):
                return TAG
        return get_full_version()
    else:
        return TAG

VERSION = get_version()

