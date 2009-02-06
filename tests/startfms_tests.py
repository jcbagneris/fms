#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Tests for fms launching module.

This is heavily borrowed from the Django web framework tests.
"""

import sys
import os
import unittest

class LauncherTests(unittest.TestCase):
    """
    Base class for testing lauching module.
    """
    def run_test(self, script, args):
        """
        Run the script and return stdout and stderr flows
        """
        old_cwd = os.getcwd()
        test_dir = os.path.dirname(os.path.dirname(__file__))

        cmd = '%s "%s"' % (sys.executable, script)
        cmd += ''.join([' %s' % arg for arg in args])

        os.chdir(test_dir)
        try:
            from subprocess import Popen, PIPE
            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdin, stdout, stderr = (p.stdin, p.stdout, p.stderr)
        except ImportError:
            stdin, stdout, stderr = os.popen3(cmd)
        out, err = stdout.read(), stderr.read()

        os.chdir(old_cwd)

        return out, err

    def run_startfms(self, args):
        return self.run_test('startfms.py', args)

    def assert_output(self, stream, msg):
        """
        Utility assertion: assert that the given message exists in the output
        """
        self.failUnless(msg in stream, 
                "'%s' does not match actual output text '%s'" % (msg, stream))
        
    def assert_no_output(self, stream):
        """
        Utility assertion: assert that the given stream is empty
        """
        self.assertEquals(len(stream), 0, 
                "Stream should be empty: actually contains '%s'" % stream)

    def test_missing_command_name(self):
        """
        Return usage message and error on missing command name.
        """
        out, err = self.run_startfms([])
        self.assert_output(err, 'CRITICAL - fms - Missing command name.')
        self.assert_output(out, 
                'Usage: startfms.py [options] [command] simulationconffile')

    def test_unknown_command_name(self):
        """
        Return error message on bad command name
        """
        out, err = self.run_startfms(['badcommand'])
        self.assert_no_output(out)
        self.assert_output(err,
                'CRITICAL - fms - Unknown command: badcommand')

    def test_no_experiment_file_name(self):
        """
        Return error message on missing experiment config file
        """
        out, err = self.run_startfms(['check'])
        self.assert_no_output(out)
        self.assert_output(err,
                'CRITICAL - fms - Missing simulation config file name.')

    def test_bad_option(self):
        """
        Return error message on bad option
        """
        out, err = self.run_startfms(['--badoption', 'check'])
        self.assert_output(err, 
                'Usage: startfms.py [options] [command] simulationconffile')
        self.assert_output(err,
                'startfms.py: error: no such option: --badoption')

    def test_version_option(self):
        """
        --version should return version info
        """
        out, err = self.run_startfms(['--version'])
        self.assert_output(err,
                'INFO - fms - This is FMS v')

    def test_verbose_option(self):
        """
        -v or --verbose set loglevel to INFO
        """
        configfile = 'tests/fixtures/minimalconfig.yml'
        for option in ('-v', '--verbose'):
            out, err = self.run_startfms([option, 'check', configfile])
            self.assert_output(err,
            'INFO - fms.utils - Reading config file tests/fixtures/minimalconf')

    def test_loglevel_option(self):
        """
        -L or --loglevel set loglevel
        """
        configfile = 'tests/fixtures/minimalconfig.yml'
        for option in ('-L', '--loglevel'):
            out, err = self.run_startfms([option, 'debug', 'check', configfile])
            self.assert_output(err,
                'DEBUG - fms - Calling YamlParamsParser on')
        
    def test_showbooks_option(self):
        """
        --show-books or --show-limits show orders books
        """
        configfile = 'tests/fixtures/minimalconfig.yml'
        for option in ('--show-books', '--show-limits'):
            out, err = self.run_startfms([option, 'check', configfile])
            self.assert_no_output(out)
            out, err = self.run_startfms([option, 'run', configfile])
            self.assert_output(out,
                    'Price | Quantity |     Emitter')

    def test_orderslogfilename_option(self):
        """
        --orderslogfilename option overrides config parameter
        """
        configfile = 'tests/fixtures/fullconfig.yml'
        out, err = self.run_startfms(['-v', '--orderslogfilename', 'afile.log', 
            'check', configfile])
        self.assert_output(err, 'afile.log')

    def test_outputfilename_option(self):
        """
        -o or --outputfilename overrides config parameter
        """
        configfile = 'tests/fixtures/fullconfig.yml'
        for option in ('-o', '--outputfilename'):
            out, err = self.run_startfms(['-v', option, 'afile.csv',
                'check', configfile])
            self.assert_output(err, 'afile.csv')


    def test_replay_option(self):
        """
        --replay or -r overrides agent config parameters
        """
        configfile = 'tests/fixtures/fullconfig.yml'
        for option in ('-r', '--replay'):
            out, err = self.run_startfms(['-v', option, 'check', configfile])
            self.assert_output(err,
                    'INFO - fms.utils - orderslogfilename : None')
            self.assert_output(err,
                    '1 PlayOrderLogFile')
            self.assert_output(err,
                    '/dummyoutput.log\']')

    def test_timer_option(self):
        """
        -t or --timer show timer during run
        """
        configfile = 'tests/fixtures/fullconfig.yml'
        for option in ('-t', '--timer'):
            out, err = self.run_startfms([option, '-o sys.stdout',
                '--orderslogfile None', 'run', configfile])
            self.assert_output(err, "0002:00010")


if __name__ == "__main__":
    unittest.main()
