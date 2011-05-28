#!/usr/bin/env python
"""
FMS git bindings
"""
import os

from subprocess import Popen, PIPE

def get_git_repo():
    """
    Return fms git repo path, if any
    """
    try:
        fms_real_path = os.path.realpath(__file__)
        fms_real_path = fms_real_path.rsplit(os.sep, 3)[0]
    except IOError:
        return False
    repo = os.path.join(fms_real_path, '.git')
    if os.path.exists(repo):
        #print repo
        return repo
    return None

def is_git_repo():
    """
    True if fms dir is a git repo
    """
    return get_git_repo() is not None

def get_git_commit_hash(tag=None):
    """
    use git rev-parse to get given commit hash
    """
    repo = get_git_repo()
    if not repo:
        return None
    if not tag:
        tag = 'HEAD'
    try:
        commit = Popen(["git","rev-parse",tag], stdout=PIPE, cwd=repo).communicate()[0].strip()
    except:
        commit = None
    return commit

def get_git_status():
    """
    return git status output
    """
    repo = get_git_repo()
    if not repo:
        return None
    repo = repo.rsplit(os.sep, 1)[0]
    try:
        status = Popen(["git","status","--porcelain"], stdout=PIPE, cwd=repo).communicate()[0].strip()
    except:
        status = False
    return status

def is_repo_clean():
    """
    True if git repo is clean
    """
    if not is_git_repo():
        return True
    return get_git_status() == ''

