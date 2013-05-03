#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Make prettier file names.  Gets rid of spaces, underscores and capital
leters, and uses dashes to separate words.

Usage:

dashify [options] file[s]

Options:

-h, --help        This help
-s, --silent      Keep quiet
-r, --recursive   Rename recursively
-t                Run tests
"""

import os, re

#http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
import unicodedata
def strip_accents(s):
    #if isinstance(s, basestring):
    #    s = s.decode('utf-8')
    if isinstance(s, unicode):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')
    return s

def dash_name(name):
    """
    >>> dash_name('hola_adios')
    'hola-adios'
    >>> dash_name('hola__adios')
    'hola-adios'
    >>> dash_name('hola_-adios')
    'hola-adios'
    >>> dash_name('hola  adios')
    'hola-adios'
    >>> dash_name('holaAdios')
    'hola-adios'
    >>> dash_name('dir/holaAdios')
    'dir/hola-adios'
    >>> dash_name('this_dir/this other dir/withAFile.txt')
    'this-dir/this-other-dir/with-a-file.txt'
    >>> dash_name(u'hola-adios&crazy')
    u'hola-adios-crazy'
    >>> dash_name(u'hola-^#$adios()&Crazy')
    u'hola-adios-crazy'
    """
    name = strip_accents(name)
    name = re.sub(r'[^a-zA-Z0-9/\\\.]+', '-', name)
    name = re.sub(r'_+', '-', name)
    name = re.sub(r'([a-z])([A-Z])([A-Z])', r'\1-\2-\3', name)
    name = re.sub(r'([a-z])([A-Z])', r'\1-\2', name)
    name = re.sub(r'--+', '-', name)
    name = re.sub(r'\.-', '-', name)
    return name.lower()

def dash_file(fname, verbose=False):
    new = dash_name(fname)
    if verbose:
        print fname, '->', new
    try:
        os.rename(fname, new)
    except OSError:
        print '** ', fname
        raise
    return new

def dash_tree(dirname, verbose=False):
    """
    >>> dash_tree('test')
    4
    >>> dash_tree('test')
    0
    """
    modified = 0
    for node in os.listdir(dirname):
        node = os.path.join(dirname, node)
        dashed = dash_file(node, verbose)
        if dashed != node:
            modified += 1
        if os.path.isdir(dashed):
            modified += dash_tree(dashed, verbose)
    return modified


def _test():
    import shutil, doctest

    def touch(fname, *dirs):
        fname = os.path.join(*(list(dirs) + [fname]))
        with file(fname, 'a'):
            os.utime(fname, None)
    def mkdir(*rest):
        dname = os.path.join(*rest)
        if not os.path.exists(dname):
            os.makedirs(dname)
        return dname

    testdir = 'test'
    if os.path.exists(testdir):
        shutil.rmtree(testdir)

    d1 = mkdir(testdir, 'firstName')
    touch('firstFile', d1)
    d2 = mkdir(d1, 'secondDir')
    touch('secondFile', d2)
    import doctest
    failed = doctest.testmod()[0]
    if failed == 0:
        shutil.rmtree(testdir)
    return failed

def as_main():
    import sys
    def help():
        print __doc__

    recursive = False
    verbose = True

    from getopt import getopt
    opts, files = getopt(sys.argv[1:], 'hrst', ['help', 'recursive', 'silent'])
    for (opt, val) in opts:
        if   opt == '-h' or opt == '--help':
            help()
            sys.exit(1)
        elif opt == '-t':
            sys.exit(_test())
        elif opt == '-r' or opt == '--recursive':
            recursive = True
        elif opt == '-s' or opt == '--silent':
            verbose = False

    for f in files:
        dash_file(f, verbose)
        if recursive:
            dash_tree(f, verbose)

if __name__ == "__main__":
    #print dash_name(u'hóla–^#$adioç()&Crazy')
    as_main()
